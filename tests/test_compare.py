import pytest
from sltk.loader_metadata import StationLoader
from sltk.compare import compare_stations


@pytest.fixture
def comparison():
    loader_metadata = StationLoader('data/metadata_stations.csv')
    station_ids = [154, 2098, 2075, 2095, 2142, 2093, 2090]
    return compare_stations(loader_metadata, station_ids, data_dir='data/stations')


def test_all_stations_present(comparison):
    assert len(comparison) == 7


def test_trend_column_exists(comparison):
    assert 'trend_mm_per_year' in comparison.columns


def test_trends_are_numeric_and_finite(comparison):
    assert comparison['trend_mm_per_year'].notna().all()


def test_has_geometry_column(comparison):
    assert 'geometry' in comparison.columns