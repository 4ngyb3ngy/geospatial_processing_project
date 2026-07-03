import pytest
from sltk.loader import load_station_series
from sltk.loader_metadata import StationLoader


@pytest.fixture
def trieste_series():
    return load_station_series('data/stations/154.rlrdata.txt')


@pytest.fixture
def loader_metadata():
    return StationLoader('data/metadata_stations.csv')


def test_series_not_empty(trieste_series):
    assert not trieste_series.empty


def test_series_columns(trieste_series):
    assert set(trieste_series.columns) == {'sea_level_mm', 'interpolated_flag', 'missing_days'}


def test_no_missing_value_placeholder(trieste_series):
    assert -99999 not in trieste_series['sea_level_mm'].values


def test_date_index_is_datetime(trieste_series):
    assert trieste_series.index.dtype.kind == 'M'


def test_metadata_has_geometry_column(loader_metadata):
    assert 'geometry' in loader_metadata.metadata.columns


def test_get_station_single_id(loader_metadata):
    result = loader_metadata.get_station(154)
    assert len(result) == 1
    assert result.iloc[0]['ID'] == 154


def test_get_station_multiple_ids(loader_metadata):
    result = loader_metadata.get_station([154, 2093])
    assert len(result) == 2
    assert set(result['ID']) == {154, 2093}


def test_get_station_unknown_id_returns_empty(loader_metadata):
    result = loader_metadata.get_station(999999)
    assert result.empty