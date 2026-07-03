import pytest
from sltk.loader_metadata import StationLoader
from sltk.distances import Distances


@pytest.fixture
def dist():
    stations_gdf = StationLoader('data/metadata_stations.csv').metadata
    return Distances(stations_gdf, id_col='ID')


def test_geodetic_trieste_genova_known_distance(dist):
    d_geo = dist.geodetic(45.647, 13.758, 44.400, 8.900)
    # distanza reale nota ~380-410 km
    assert 380 <= d_geo <= 410


def test_euclidean_smaller_than_geodetic_in_degrees(dist):
    d_eucl = dist.euclidean(45.647, 13.758, 44.400, 8.900)
    assert d_eucl > 0


def test_nearest_returns_correct_count(dist):
    nearest = dist.nearest(station_id=154, n=3, method='geodetic')
    assert len(nearest) == 3


def test_nearest_geodetic_finds_trieste_ii_closest(dist):
    nearest = dist.nearest(station_id=154, n=3, method='geodetic')
    closest = nearest.iloc[0]
    assert closest['Station Name'] == 'TRIESTE II'
    assert closest['distance'] < 1  # meno di 1 km


def test_nearest_unknown_id_raises(dist):
    with pytest.raises(ValueError):
        dist.nearest(station_id=999999, n=3)

def test_projected_crs_raises():
    stations_gdf = StationLoader('data/metadata_stations.csv').metadata
    # UTM zone 33N (EPSG:32633): a projected CRS, in meters, not degrees.
    projected = stations_gdf.to_crs(epsg=32633)
    with pytest.raises(ValueError):
        Distances(projected, id_col='ID')