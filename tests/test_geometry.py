import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from sltk.geometry import p_in_poly, point_in_region, filter_stations_by_region
from sltk.loader_metadata import StationLoader


@pytest.fixture
def world():
    world = gpd.read_file('data/boundaries/ne_110m_admin_0_countries.shp')
    world = world.set_crs(epsg=4326, allow_override=True)
    return world

@pytest.fixture
def stations_gdf():
    return StationLoader('data/metadata_stations.csv').metadata


def test_p_in_poly_matches_shapely():
    polygon_test = Polygon([(1, 1), (5, 1), (5, 5), (3, 3), (1, 5)])
    point_test = Point(3, 2)
    assert p_in_poly(point_test, polygon_test) == polygon_test.contains(point_test)


def test_point_in_region_for_known_italian_station(world, stations_gdf):
    italy = world[world['SOV_A3'] == 'ITA']
    italy_geom = italy.union_all()

    mask = stations_gdf.within(italy_geom)
    italian_stations = stations_gdf[mask]

    test_point = italian_stations.geometry.iloc[0]
    assert point_in_region(test_point, italy_geom) is True


def test_filter_stations_by_region_matches_shapely_within(world, stations_gdf):
    italy_geom = world[world['SOV_A3'] == 'ITA'].union_all()
    expected = stations_gdf[stations_gdf.within(italy_geom)]

    result = filter_stations_by_region(stations_gdf, world, country_code='ITA')
    assert len(result) == len(expected)


def test_filter_stations_by_region_invalid_code_raises(world, stations_gdf):
    with pytest.raises(ValueError):
        filter_stations_by_region(stations_gdf, world, country_code='XXX')

def test_filter_stations_by_region_crs_mismatch_raises(world, stations_gdf):
    # Reproject only the stations to a different CRS (UTM 33N), so that
    # stations_gdf and world_gdf no longer share the same reference system.
    mismatched_stations = stations_gdf.to_crs(epsg=32633)
    with pytest.raises(ValueError):
        filter_stations_by_region(mismatched_stations, world, country_code='ITA')