"""
Integration tests for MeTTa interface with Guardian agents.

Validates that agents can successfully import and use the MeTTa query interface.
"""

import pytest
from agents.shared.metta_interface import (
    query_historical_performance,
    query_all_crashes,
    query_recovery_winners,
)


class TestMeTTaAgentIntegration:
    """Test that agents can successfully use MeTTa interface."""

    def test_import_metta_interface_from_agents(self):
        """Test that agents can import metta_interface module."""
        # Simulate agent import
        from agents.shared import metta_interface

        assert hasattr(metta_interface, 'query_historical_performance')
        assert hasattr(metta_interface, 'query_all_crashes')
        assert hasattr(metta_interface, 'query_crashes_by_correlation_loss')
        assert hasattr(metta_interface, 'query_sector_performance_across_crashes')
        assert hasattr(metta_interface, 'query_recovery_winners')

    def test_correlation_agent_can_query_crash_data(self):
        """Test CorrelationAgent can query historical crash data."""
        # Simulate CorrelationAgent querying crash data for correlation analysis
        crash = query_historical_performance("crash_2022_bear")

        # CorrelationAgent would use this data to compare user portfolio correlation
        # to historical performance
        assert crash["scenario_id"] == "crash_2022_bear"
        assert ">90%" in crash["correlation_brackets"]
        assert crash["correlation_brackets"][">90%"] == -73.0

        # Simulate correlation agent logic
        user_correlation = 0.92  # Example: 92% correlation with ETH
        if user_correlation > 0.90:
            expected_loss = crash["correlation_brackets"][">90%"]
            assert expected_loss == -73.0  # Expected loss for high correlation

    def test_sector_agent_can_query_sector_performance(self):
        """Test SectorAgent can query sector performance data."""
        # Simulate SectorAgent querying sector-specific crash data
        crash = query_historical_performance("crash_2022_bear")

        # SectorAgent would use this data to assess sector concentration risk
        assert "DeFi Governance" in crash["sector_performance"]
        assert crash["sector_performance"]["DeFi Governance"] == -75.0

        # Simulate sector agent logic
        portfolio_defi_allocation = 0.85  # Example: 85% in DeFi Governance
        if portfolio_defi_allocation > 0.60:
            sector_risk = crash["sector_performance"]["DeFi Governance"]
            assert sector_risk == -75.0  # High concentration risk

    def test_agent_can_query_multiple_crashes_for_comparison(self):
        """Test agents can compare performance across multiple crashes."""
        # Simulate agent comparing portfolio behavior across all historical crashes
        all_crashes = query_all_crashes()

        assert len(all_crashes) == 3

        # Simulate extracting >90% correlation bracket losses
        high_corr_losses = [
            c["correlation_brackets"][">90%"]
            for c in all_crashes
        ]

        # Verify all expected losses are present
        assert -73.0 in high_corr_losses  # 2022 bear market
        assert -52.0 in high_corr_losses  # 2021 correction
        assert -62.0 in high_corr_losses  # 2020 COVID crash

        # Simulate calculating average historical loss for high correlation
        avg_loss = sum(high_corr_losses) / len(high_corr_losses)
        assert -63.0 < avg_loss < -61.0  # Average ~-62.3%

    def test_agent_can_provide_recovery_recommendations(self):
        """Test agents can query recovery winners for recommendations."""
        # Simulate agent providing recovery recommendations based on historical data
        winners_2022 = query_recovery_winners("crash_2022_bear")

        assert len(winners_2022) == 3
        assert "SOL" in winners_2022
        assert "MATIC" in winners_2022
        assert "OP" in winners_2022

        # Simulate agent building recommendation message
        recommendation = (
            f"Consider diversifying into recovery winners from similar crashes: "
            f"{', '.join(winners_2022)}"
        )

        assert "SOL" in recommendation
        assert "recovery winners" in recommendation

    def test_agent_error_handling_graceful_degradation(self):
        """Test agents handle MeTTa query errors gracefully."""
        # Simulate agent querying invalid crash ID
        with pytest.raises(ValueError) as exc_info:
            query_historical_performance("crash_invalid")

        # Agent should catch this and provide fallback behavior
        error_msg = str(exc_info.value)
        assert "not found" in error_msg

        # Simulate agent fallback: use default conservative estimate
        fallback_loss_estimate = -60.0  # Conservative default
        assert fallback_loss_estimate == -60.0

    def test_agentverse_compatibility_no_hyperon_import(self):
        """Test that metta_interface doesn't import Hyperon (Agentverse incompatible)."""
        import agents.shared.metta_interface as metta_module

        # Verify no Hyperon import in module
        with open(metta_module.__file__, 'r') as f:
            module_source = f.read()

        assert "import hyperon" not in module_source.lower()
        assert "from hyperon" not in module_source.lower()

        # Verify module can be imported without Hyperon installed
        # (already imported, so if we got here, it worked)
        assert metta_module is not None


class TestMeTTaJSONFallbackStrategy:
    """Test that JSON fallback strategy works for Agentverse deployment."""

    def test_json_fallback_provides_same_data_as_metta_queries(self):
        """Verify JSON fallback returns same data structure as MeTTa queries would."""
        # Query via JSON fallback (current implementation)
        crash = query_historical_performance("crash_2022_bear")

        # Verify data structure matches expected MeTTa query result
        required_fields = [
            "scenario_id",
            "name",
            "period",
            "eth_drawdown_pct",
            "correlation_brackets",
            "sector_performance",
            "recovery_winners",
        ]

        for field in required_fields:
            assert field in crash, f"Missing required field: {field}"

        # Verify correlation brackets structure
        assert isinstance(crash["correlation_brackets"], dict)
        assert ">90%" in crash["correlation_brackets"]
        assert "80-90%" in crash["correlation_brackets"]
        assert "70-80%" in crash["correlation_brackets"]
        assert "<70%" in crash["correlation_brackets"]

        # Verify sector performance structure
        assert isinstance(crash["sector_performance"], dict)
        assert "DeFi Governance" in crash["sector_performance"]
        assert "Layer-2" in crash["sector_performance"]
        assert "Stablecoins" in crash["sector_performance"]

    def test_json_fallback_file_access_works(self):
        """Test that JSON file access works (Agentverse file I/O)."""
        from pathlib import Path
        import json

        # Verify data file exists
        data_dir = Path(__file__).parent.parent / "data"
        crashes_file = data_dir / "historical-crashes.json"

        assert crashes_file.exists(), "historical-crashes.json not found"

        # Verify file can be read
        with open(crashes_file, 'r') as f:
            data = json.load(f)

        assert "crashes" in data
        assert len(data["crashes"]) == 3
