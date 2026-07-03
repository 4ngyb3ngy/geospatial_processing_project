import pytest
from sltk.analysis import SeaLevelAnalysis
from sltk.loader import load_station_series


@pytest.fixture
def trieste_analysis():
    series = load_station_series('data/stations/154.rlrdata.txt')
    return SeaLevelAnalysis(series['sea_level_mm'])


def test_compute_trend_positive(trieste_analysis):
    result = trieste_analysis.compute_trend()
    assert result['trend_mm_per_year'] > 0


def test_compute_trend_significant(trieste_analysis):
    result = trieste_analysis.compute_trend()
    assert result['p_value'] < 0.05


def test_compute_trend_expected_range(trieste_analysis):
    result = trieste_analysis.compute_trend()
    # trend noto per Trieste ~1.35 mm/anno, tolleranza ampia
    assert 0.5 < result['trend_mm_per_year'] < 3.0


def test_seasonal_cycle_has_twelve_months(trieste_analysis):
    cycle = trieste_analysis.seasonal_cycle()
    assert len(cycle) == 12


def test_seasonal_cycle_index_range(trieste_analysis):
    cycle = trieste_analysis.seasonal_cycle()
    assert set(cycle.index) == set(range(1, 13))