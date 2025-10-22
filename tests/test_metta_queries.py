"""
Unit tests for MeTTa knowledge graph query interface.

Tests verify that MeTTa query functions return accurate results for known
crash scenarios and that data consistency is maintained with historical-crashes.json.
"""

import pytest
from unittest.mock import patch, mock_open
import json

from agents.shared.metta_interface import (
    query_historical_performance,
    query_all_crashes,
    query_crashes_by_correlation_loss,
    query_sector_performance_across_crashes,
    query_recovery_winners,
    MeTTaQueryError,
)


class TestQueryHistoricalPerformance:
    """Test query_historical_performance function."""

    def test_query_2022_crash(self):
        """Test 2022 bear market crash query returns correct data."""
        result = query_historical_performance("crash_2022_bear")

        assert result["scenario_id"] == "crash_2022_bear"
        assert result["name"] == "2022 Bear Market"
        assert result["period"] == "Nov 2021 - Jun 2022"
        assert result["eth_drawdown_pct"] == -75.0
        assert result["market_avg_loss_pct"] == -55.0
        assert result["recovery_period"] == "Jun 2022 - Dec 2023"

        # Verify correlation brackets
        assert result["correlation_brackets"][">90%"] == -73.0
        assert result["correlation_brackets"]["80-90%"] == -68.0
        assert result["correlation_brackets"]["70-80%"] == -62.0
        assert result["correlation_brackets"]["<70%"] == -48.0

        # Verify sector performance
        assert result["sector_performance"]["DeFi Governance"] == -75.0
        assert result["sector_performance"]["Layer-2"] == -60.0
        assert result["sector_performance"]["Yield Protocols"] == -80.0
        assert result["sector_performance"]["Stablecoins"] == -5.0

        # Verify recovery winners
        assert "SOL" in result["recovery_winners"]
        assert "MATIC" in result["recovery_winners"]
        assert "OP" in result["recovery_winners"]

    def test_query_2021_correction(self):
        """Test 2021 correction crash query returns correct data."""
        result = query_historical_performance("crash_2021_correction")

        assert result["scenario_id"] == "crash_2021_correction"
        assert result["name"] == "2021 Correction"
        assert result["period"] == "May 2021 - Jul 2021"
        assert result["eth_drawdown_pct"] == -55.0
        assert result["correlation_brackets"][">90%"] == -52.0
        assert result["sector_performance"]["DeFi Governance"] == -58.0

    def test_query_2020_covid_crash(self):
        """Test 2020 COVID crash query returns correct data."""
        result = query_historical_performance("crash_2020_covid")

        assert result["scenario_id"] == "crash_2020_covid"
        assert result["name"] == "2020 COVID Crash"
        assert result["period"] == "Feb 2020 - Mar 2020"
        assert result["eth_drawdown_pct"] == -65.0
        assert result["correlation_brackets"][">90%"] == -62.0
        assert result["sector_performance"]["DeFi Governance"] == -48.0

    def test_query_invalid_crash_id(self):
        """Test querying non-existent crash raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            query_historical_performance("crash_nonexistent")

        assert "not found in MeTTa knowledge graph" in str(exc_info.value)
        assert "crash_2022_bear" in str(exc_info.value)  # Should list available IDs

    def test_query_with_correlation_bracket_filter(self):
        """Test query with correlation bracket parameter (filter logged but data returned)."""
        result = query_historical_performance(
            "crash_2022_bear",
            correlation_bracket=">90%"
        )

        # Function returns full crash data; caller applies filter
        assert result["scenario_id"] == "crash_2022_bear"
        assert ">90%" in result["correlation_brackets"]
        assert result["correlation_brackets"][">90%"] == -73.0

    def test_query_with_sector_filter(self):
        """Test query with sector parameter (filter logged but data returned)."""
        result = query_historical_performance(
            "crash_2022_bear",
            sector="DeFi Governance"
        )

        # Function returns full crash data; caller applies filter
        assert result["scenario_id"] == "crash_2022_bear"
        assert "DeFi Governance" in result["sector_performance"]
        assert result["sector_performance"]["DeFi Governance"] == -75.0


class TestQueryAllCrashes:
    """Test query_all_crashes function."""

    def test_query_all_crashes_returns_three_scenarios(self):
        """Test that all 3 crash scenarios are returned."""
        crashes = query_all_crashes()

        assert len(crashes) == 3

        scenario_ids = [c["scenario_id"] for c in crashes]
        assert "crash_2022_bear" in scenario_ids
        assert "crash_2021_correction" in scenario_ids
        assert "crash_2020_covid" in scenario_ids

    def test_all_crashes_have_required_fields(self):
        """Test that all crashes have required data fields."""
        crashes = query_all_crashes()

        required_fields = [
            "scenario_id",
            "name",
            "period",
            "eth_drawdown_pct",
            "correlation_brackets",
            "sector_performance",
            "recovery_winners",
        ]

        for crash in crashes:
            for field in required_fields:
                assert field in crash, f"Missing field '{field}' in {crash['scenario_id']}"


class TestQueryCrashesByCorrelationLoss:
    """Test query_crashes_by_correlation_loss function."""

    def test_find_crashes_with_high_correlation_loss_above_70(self):
        """Test finding crashes where >90% correlation bracket lost more than 70%."""
        results = query_crashes_by_correlation_loss(">90%", -70.0)

        # Only 2022 bear market has >90% bracket at -73.0 (below -70.0)
        assert len(results) == 1
        assert results[0]["scenario_id"] == "crash_2022_bear"
        assert results[0]["correlation_brackets"][">90%"] == -73.0

    def test_find_crashes_with_medium_high_correlation_loss(self):
        """Test finding crashes where 80-90% bracket lost more than 60%."""
        results = query_crashes_by_correlation_loss("80-90%", -60.0)

        # 2022 bear market: -68.0 (below -60.0) ✓
        # 2021 correction: -48.0 (above -60.0) ✗
        # 2020 covid: -58.0 (above -60.0) ✗
        assert len(results) == 1
        assert results[0]["scenario_id"] == "crash_2022_bear"

    def test_find_no_crashes_with_impossible_threshold(self):
        """Test query with threshold that no crash meets."""
        results = query_crashes_by_correlation_loss(">90%", -80.0)
        assert len(results) == 0  # No crash has >90% bracket below -80%


class TestQuerySectorPerformanceAcrossCrashes:
    """Test query_sector_performance_across_crashes function."""

    def test_query_defi_governance_sector_across_all_crashes(self):
        """Test getting DeFi Governance performance across all crashes."""
        results = query_sector_performance_across_crashes("DeFi Governance")

        assert len(results) == 3

        # Extract losses by crash
        losses_by_crash = {r["crash_id"]: r["sector_loss"] for r in results}

        assert losses_by_crash["crash_2022_bear"] == -75.0
        assert losses_by_crash["crash_2021_correction"] == -58.0
        assert losses_by_crash["crash_2020_covid"] == -48.0

    def test_query_layer2_sector_across_all_crashes(self):
        """Test getting Layer-2 performance across all crashes."""
        results = query_sector_performance_across_crashes("Layer-2")

        assert len(results) == 3

        losses_by_crash = {r["crash_id"]: r["sector_loss"] for r in results}
        assert losses_by_crash["crash_2022_bear"] == -60.0
        assert losses_by_crash["crash_2021_correction"] == -52.0
        assert losses_by_crash["crash_2020_covid"] == -55.0

    def test_query_stablecoins_sector(self):
        """Test stablecoins sector shows minimal losses."""
        results = query_sector_performance_across_crashes("Stablecoins")

        assert len(results) == 3

        # Stablecoins should have minimal losses
        for result in results:
            assert result["sector_loss"] > -10.0  # All stablecoin losses < 10%


class TestQueryRecoveryWinners:
    """Test query_recovery_winners function."""

    def test_query_recovery_winners_2022_crash(self):
        """Test recovery winners for 2022 bear market."""
        winners = query_recovery_winners("crash_2022_bear")

        assert len(winners) == 3
        assert "SOL" in winners
        assert "MATIC" in winners
        assert "OP" in winners

    def test_query_recovery_winners_2021_correction(self):
        """Test recovery winners for 2021 correction."""
        winners = query_recovery_winners("crash_2021_correction")

        assert len(winners) == 3
        assert "BNB" in winners
        assert "ADA" in winners
        assert "DOT" in winners

    def test_query_recovery_winners_2020_covid(self):
        """Test recovery winners for 2020 COVID crash."""
        winners = query_recovery_winners("crash_2020_covid")

        assert len(winners) == 3
        assert "LINK" in winners
        assert "UNI" in winners
        assert "AAVE" in winners

    def test_query_recovery_winners_invalid_crash(self):
        """Test querying recovery winners for invalid crash raises error."""
        with pytest.raises(ValueError):
            query_recovery_winners("crash_nonexistent")


class TestMeTTaDataConsistency:
    """Test consistency between MeTTa queries and historical-crashes.json."""

    def test_metta_json_consistency_all_crashes(self):
        """Verify MeTTa results exactly match source JSON data."""
        crashes = query_all_crashes()

        # Load source JSON directly
        import json
        from pathlib import Path

        data_dir = Path(__file__).parent.parent / "data"
        with open(data_dir / "historical-crashes.json") as f:
            source_data = json.load(f)

        source_crashes = source_data["crashes"]

        # Compare counts
        assert len(crashes) == len(source_crashes)

        # Compare each crash in detail
        for i, crash in enumerate(crashes):
            source_crash = source_crashes[i]

            # Compare all fields exactly
            assert crash["scenario_id"] == source_crash["scenario_id"]
            assert crash["name"] == source_crash["name"]
            assert crash["period"] == source_crash["period"]
            assert crash["eth_drawdown_pct"] == source_crash["eth_drawdown_pct"]

            # Compare correlation brackets
            for bracket in [">90%", "80-90%", "70-80%", "<70%"]:
                assert crash["correlation_brackets"][bracket] == source_crash["correlation_brackets"][bracket]

            # Compare sector performance
            for sector in crash["sector_performance"].keys():
                assert crash["sector_performance"][sector] == source_crash["sector_performance"][sector]

            # Compare recovery winners
            assert crash["recovery_winners"] == source_crash["recovery_winners"]


class TestMeTTaErrorHandling:
    """Test error handling in MeTTa query functions."""

    def test_missing_data_file_raises_error(self):
        """Test that missing data file raises MeTTaQueryError."""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with pytest.raises(MeTTaQueryError) as exc_info:
                query_all_crashes()

            assert "not found" in str(exc_info.value)

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises MeTTaQueryError."""
        invalid_json = "{ invalid json }"

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with pytest.raises(MeTTaQueryError) as exc_info:
                query_all_crashes()

            assert "parse" in str(exc_info.value).lower()


class TestMeTTaLogging:
    """Test that MeTTa queries log appropriately."""

    def test_query_logs_info_message(self, caplog):
        """Test that queries log INFO level messages."""
        import logging
        caplog.set_level(logging.INFO)

        query_historical_performance("crash_2022_bear")

        # Check that INFO log messages were generated
        assert any("Querying MeTTa knowledge graph" in record.message for record in caplog.records)
        assert any("MeTTa query successful" in record.message for record in caplog.records)

    def test_query_all_crashes_logs_count(self, caplog):
        """Test that query_all_crashes logs the count of crashes retrieved."""
        import logging
        caplog.set_level(logging.INFO)

        query_all_crashes()

        # Should log the count of crashes
        assert any("3 crash scenarios" in record.message for record in caplog.records)
