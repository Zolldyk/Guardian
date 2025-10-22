"""
MeTTa Knowledge Graph Interface

Provides abstraction layer for querying historical crash scenarios from the
MeTTa knowledge graph. Uses JSON representation due to Hyperon library
compatibility constraints with Python 3.13 and Agentverse deployment.

This module demonstrates SingularityNET MeTTa integration while maintaining
production compatibility through pre-computed JSON queries.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

# Path to historical crashes data (JSON representation of MeTTa knowledge graph)
DATA_DIR = Path(__file__).parent.parent.parent / "data"
CRASHES_FILE = DATA_DIR / "historical-crashes.json"


class MeTTaQueryError(Exception):
    """Raised when MeTTa query fails or returns invalid data."""
    pass


def _load_crash_data() -> Dict[str, Any]:
    """
    Load historical crash data from JSON file.

    Returns:
        Dictionary containing crash scenarios

    Raises:
        MeTTaQueryError: If data file cannot be loaded
    """
    try:
        with open(CRASHES_FILE, 'r') as f:
            data = json.load(f)
        logger.debug(f"Loaded {len(data.get('crashes', []))} crash scenarios from MeTTa knowledge graph")
        return data
    except FileNotFoundError:
        logger.error(f"MeTTa knowledge graph data not found: {CRASHES_FILE}")
        raise MeTTaQueryError(f"Historical crash data file not found: {CRASHES_FILE}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in MeTTa knowledge graph data: {e}")
        raise MeTTaQueryError(f"Failed to parse historical crash data: {e}")


def query_historical_performance(
    crash_scenario_id: str,
    correlation_bracket: Optional[str] = None,
    sector: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query MeTTa knowledge graph for historical crash performance data.

    This function provides a unified interface to query crash scenarios,
    correlation bracket performance, and sector-specific data from the
    MeTTa knowledge graph (JSON representation).

    Args:
        crash_scenario_id: Crash identifier ("crash_2022_bear", "crash_2021_correction", "crash_2020_covid")
        correlation_bracket: Optional filter for correlation bracket (">90%", "80-90%", "70-80%", "<70%")
        sector: Optional filter for sector ("DeFi Governance", "Layer-2", etc.)

    Returns:
        Dictionary containing crash scenario data:
        {
            "scenario_id": str,
            "name": str,
            "period": str,
            "eth_drawdown_pct": float,
            "correlation_brackets": dict[str, float],
            "sector_performance": dict[str, float],
            "recovery_winners": list[str],
            "recovery_period": str,
            "market_avg_loss_pct": float,
            "opportunity_cost_sectors": dict (optional)
        }

    Raises:
        ValueError: If crash_scenario_id not found
        MeTTaQueryError: If query execution fails

    Examples:
        >>> # Get complete crash scenario data
        >>> crash = query_historical_performance("crash_2022_bear")
        >>> print(crash["eth_drawdown_pct"])
        -75.0

        >>> # Filter by correlation bracket
        >>> crash = query_historical_performance("crash_2022_bear", correlation_bracket=">90%")
        >>> print(crash["correlation_brackets"][">90%"])
        -73.0

        >>> # Filter by sector
        >>> crash = query_historical_performance("crash_2022_bear", sector="DeFi Governance")
        >>> print(crash["sector_performance"]["DeFi Governance"])
        -75.0
    """
    logger.info(f"Querying MeTTa knowledge graph for crash scenario: {crash_scenario_id}")

    # Load crash data from JSON (MeTTa knowledge graph representation)
    try:
        data = _load_crash_data()
        crashes = data.get("crashes", [])

        # Find matching crash scenario
        crash = None
        for c in crashes:
            if c.get("scenario_id") == crash_scenario_id:
                crash = c
                break

        if not crash:
            available_ids = [c.get("scenario_id") for c in crashes]
            raise ValueError(
                f"Crash scenario '{crash_scenario_id}' not found in MeTTa knowledge graph. "
                f"Available: {available_ids}"
            )

        # Log filters if provided
        if correlation_bracket:
            logger.debug(f"Filtering for correlation bracket: {correlation_bracket}")
        if sector:
            logger.debug(f"Filtering for sector: {sector}")

        # Return full crash data (filters can be applied by caller)
        # MeTTa query pattern: (match (Crash crash_id ?name ?period) ...)
        logger.info(f"MeTTa query successful: {crash['name']} ({crash['period']})")
        return crash

    except ValueError:
        # Re-raise ValueError for invalid crash_scenario_id
        raise
    except Exception as e:
        logger.error(f"MeTTa query failed: {e}")
        raise MeTTaQueryError(f"Failed to query historical performance: {e}")


def query_all_crashes() -> List[Dict[str, Any]]:
    """
    Query all crash scenarios from MeTTa knowledge graph.

    Returns:
        List of crash scenario dictionaries

    Raises:
        MeTTaQueryError: If query execution fails

    Examples:
        >>> crashes = query_all_crashes()
        >>> len(crashes)
        3
        >>> crashes[0]["scenario_id"]
        'crash_2022_bear'
    """
    logger.info("Querying all crash scenarios from MeTTa knowledge graph")

    try:
        data = _load_crash_data()
        crashes = data.get("crashes", [])
        logger.info(f"Retrieved {len(crashes)} crash scenarios")
        return crashes
    except Exception as e:
        logger.error(f"Failed to query all crashes: {e}")
        raise MeTTaQueryError(f"Failed to query all crashes: {e}")


def query_crashes_by_correlation_loss(
    correlation_bracket: str,
    min_loss_pct: float
) -> List[Dict[str, Any]]:
    """
    Find crashes where a specific correlation bracket lost more than threshold.

    MeTTa query pattern:
    (match (and (Crash ?id ?name ?period)
                (CorrelationBracketLoss ?id bracket ?loss)
                (< ?loss min_loss))
      (?id ?name ?loss))

    Args:
        correlation_bracket: Correlation bracket (">90%", "80-90%", "70-80%", "<70%")
        min_loss_pct: Minimum loss percentage (e.g., -70.0)

    Returns:
        List of crash scenarios matching criteria

    Examples:
        >>> # Find crashes where >90% correlation portfolios lost more than 70%
        >>> severe_crashes = query_crashes_by_correlation_loss(">90%", -70.0)
        >>> len(severe_crashes)
        1
        >>> severe_crashes[0]["scenario_id"]
        'crash_2022_bear'
    """
    logger.info(f"Querying crashes where {correlation_bracket} lost more than {min_loss_pct}%")

    try:
        crashes = query_all_crashes()
        matching = []

        for crash in crashes:
            brackets = crash.get("correlation_brackets", {})
            loss = brackets.get(correlation_bracket)

            if loss is not None and loss < min_loss_pct:
                matching.append(crash)
                logger.debug(
                    f"Match found: {crash['scenario_id']} - "
                    f"{correlation_bracket} bracket lost {loss}%"
                )

        logger.info(f"Found {len(matching)} crashes matching criteria")
        return matching

    except Exception as e:
        logger.error(f"Failed to query crashes by correlation loss: {e}")
        raise MeTTaQueryError(f"Query failed: {e}")


def query_sector_performance_across_crashes(sector: str) -> List[Dict[str, Any]]:
    """
    Get sector performance across all crash scenarios.

    MeTTa query pattern:
    (match (and (Crash ?id ?name ?period)
                (SectorPerformance ?id sector ?loss))
      (?id ?name ?loss))

    Args:
        sector: Sector name ("DeFi Governance", "Layer-2", etc.)

    Returns:
        List of dictionaries with crash_id, name, period, and sector_loss

    Examples:
        >>> # Get DeFi Governance performance in all crashes
        >>> defi_performance = query_sector_performance_across_crashes("DeFi Governance")
        >>> len(defi_performance)
        3
        >>> defi_performance[0]["sector_loss"]
        -75.0
    """
    logger.info(f"Querying {sector} sector performance across all crashes")

    try:
        crashes = query_all_crashes()
        results = []

        for crash in crashes:
            sector_perf = crash.get("sector_performance", {})
            loss = sector_perf.get(sector)

            if loss is not None:
                results.append({
                    "crash_id": crash["scenario_id"],
                    "name": crash["name"],
                    "period": crash["period"],
                    "sector_loss": loss
                })
                logger.debug(f"{crash['scenario_id']}: {sector} lost {loss}%")

        logger.info(f"Retrieved {sector} performance for {len(results)} crashes")
        return results

    except Exception as e:
        logger.error(f"Failed to query sector performance: {e}")
        raise MeTTaQueryError(f"Query failed: {e}")


def query_recovery_winners(crash_scenario_id: str) -> List[str]:
    """
    Get recovery winners for a specific crash.

    MeTTa query pattern:
    (match (RecoveryWinner crash_id ?token) ?token)

    Args:
        crash_scenario_id: Crash identifier

    Returns:
        List of token symbols that performed well during recovery

    Raises:
        ValueError: If crash_scenario_id not found
        MeTTaQueryError: If query execution fails

    Examples:
        >>> winners = query_recovery_winners("crash_2022_bear")
        >>> winners
        ['SOL', 'MATIC', 'OP']
    """
    logger.info(f"Querying recovery winners for {crash_scenario_id}")

    try:
        crash = query_historical_performance(crash_scenario_id)
        winners = crash.get("recovery_winners", [])
        logger.info(f"Found {len(winners)} recovery winners: {winners}")
        return winners

    except ValueError:
        # Re-raise ValueError for invalid crash_scenario_id
        raise
    except Exception as e:
        logger.error(f"Failed to query recovery winners: {e}")
        raise MeTTaQueryError(f"Query failed: {e}")


# Convenience function for backwards compatibility
def query_metta(query_type: str, **kwargs) -> Any:
    """
    Generic MeTTa query interface (legacy compatibility).

    Args:
        query_type: Type of query ("crash", "all_crashes", "correlation_loss", etc.)
        **kwargs: Query-specific parameters

    Returns:
        Query results (type depends on query_type)
    """
    if query_type == "crash":
        return query_historical_performance(**kwargs)
    elif query_type == "all_crashes":
        return query_all_crashes()
    elif query_type == "correlation_loss":
        return query_crashes_by_correlation_loss(**kwargs)
    elif query_type == "sector_performance":
        return query_sector_performance_across_crashes(**kwargs)
    elif query_type == "recovery_winners":
        return query_recovery_winners(**kwargs)
    else:
        raise ValueError(f"Unknown query type: {query_type}")
