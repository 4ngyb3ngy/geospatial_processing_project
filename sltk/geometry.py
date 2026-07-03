from shapely.geometry import Point, Polygon, MultiPolygon


def p_in_poly(point, pgon):
    """
    Note: This function take inspiration from the code presented in the Course of Geospatial Processing
    taking place in Politecnico di Milano that present the Even-odd algorithm implementation
    
    Determine whether a point lies inside a polygon using the
    Even-Odd (Ray Casting) algorithm.

    Parameters
    ----------
    point : shapely.geometry.Point
        The point to test.
    pgon : shapely.geometry.Polygon
        The polygon to test against (single polygon, no holes handled here).

    Returns
    -------
    bool
        True if the point is inside the polygon, False otherwise.
    """
    numvert = len(pgon.exterior.coords) - 1
    tx = point.x
    ty = point.y

    p1 = pgon.exterior.coords[numvert - 1]
    yflag1 = (p1[1] >= ty)
    inside_flag = False

    for j in range(numvert):
        p2 = pgon.exterior.coords[j]
        yflag2 = (p2[1] >= ty)

        if yflag1 != yflag2:
            xflag1 = (p1[0] >= tx)
            xflag2 = (p2[0] >= tx)

            if xflag1 == xflag2:
                if xflag1:
                    inside_flag = not inside_flag
            else:
                m = p2[0] - (p2[1] - ty) * (p1[0] - p2[0]) / (p1[1] - p2[1])
                if m >= tx:
                    inside_flag = not inside_flag

        yflag1 = yflag2
        p1 = p2

    return inside_flag


def point_in_region(point, region_geometry):
    """
    NOTE: this is an extension of the code presented above for MultiPolygon geometry
    ex. Italy plus the italian island such as Sicily or Sardinia 
    
    Determine whether a point lies inside a region, handling both
    Polygon and MultiPolygon geometries.

    Parameters
    ----------
    point : shapely.geometry.Point
        The point to test.
    region_geometry : shapely.geometry.Polygon or shapely.geometry.MultiPolygon
        The region to test against. If it's a MultiPolygon (e.g. a country
        with islands), the point is checked against each sub-polygon.

    Returns
    -------
    bool
        True if the point is inside the region (or any of its sub-polygons), False otherwise.
    """
    if isinstance(region_geometry, MultiPolygon):
        return any(p_in_poly(point, poly) for poly in region_geometry.geoms)
    return p_in_poly(point, region_geometry)


def filter_stations_by_region(stations_gdf, world_gdf, country_code, code_col='SOV_A3'):
    """
    Filter stations that fall within a specific country/region, using the
    custom point_in_region algorithm (not shapely's built-in .within()).


    Parameters
    ----------
    stations_gdf : geopandas.GeoDataFrame
        GeoDataFrame of stations, with a 'geometry' column of Point objects.
    world_gdf : geopandas.GeoDataFrame
        GeoDataFrame of world boundaries (e.g. countries), with a
        'geometry' column of Polygon/MultiPolygon objects.
    country_code : str
        Code identifying the target country/region (e.g. 'ITA').
    code_col : str, optional
        Name of the column in world_gdf that contains the country code
        (default is 'SOV_A3').
        'SOV_A3 is the code representing the country

    Returns
    -------
    geopandas.GeoDataFrame
        Subset of stations_gdf whose geometry falls within the target region.

    Raises
    ------
    ValueError
        If no region matching country_code is found in world_gdf, or if
        stations_gdf and world_gdf do not share the same CRS.
    """
    # NOTE: p_in_poly/point_in_region compare raw coordinate values with no
    # knowledge of CRS (plain shapely geometries carry no CRS information).
    # If stations_gdf and world_gdf were in different CRSs, their coordinates
    # would be numerically comparable but geographically meaningless, and the
    # ray-casting would silently return wrong results. This check fails fast
    # instead of letting that happen unnoticed.
    
    if stations_gdf.crs != world_gdf.crs:
        raise ValueError(
            f"stations_gdf and world_gdf must share the same CRS "
            f"(got {stations_gdf.crs} and {world_gdf.crs}). "
            f"Reproject one of them with .to_crs() before calling this function."
        )

    region = world_gdf[world_gdf[code_col] == country_code]

    if region.empty:
        raise ValueError(f"Country code '{country_code}' not found in world_gdf.")

    region_geometry = region.union_all()
    mask = stations_gdf.geometry.apply(lambda p: point_in_region(p, region_geometry))

    return stations_gdf[mask]