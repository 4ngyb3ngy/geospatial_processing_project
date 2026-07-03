import numpy as np


class Distances:
    """
    Compute distances between geographic points and find nearest
    stations, using either Euclidean or geodetic (Haversine) distance.

    NOTE: it's known that the Euclidian distance is not a proper measure but here 
    is reported since it's interesting to have a comparison and a real proof of the 
    differences wrt the geodetic one

    Parameters
    ----------
    stations_gdf : geopandas.GeoDataFrame
        Station metadata with a 'geometry' column (Point) and an ID column.
    id_col : str
        Name of the column containing the station ID. Default 'ID'.
    """

    EARTH_RADIUS_KM = 6371.0  # mean Earth radius (km), used in the Haversine formula

    # NOTE: geodetic() assumes lat/lon in decimal degrees (EPSG:4326 / WGS84).
    # If stations_gdf were reprojected to a projected CRS (e.g. UTM, in meters),
    # this formula would give wrong results — it does not check or convert the CRS.

    def __init__(self, stations_gdf, id_col='ID'):
        if stations_gdf.crs is None or not stations_gdf.crs.is_geographic:
            raise ValueError(
                "Distances requires a geographic CRS (lat/lon in decimal degrees, "
                "e.g. EPSG:4326). Reproject stations_gdf before using this class."
            )
        self.stations = stations_gdf
        self.id_col = id_col
    
    def euclidean(self, lat1, lon1, lat2, lon2):
        """
        Compute the Euclidean (planar) distance between two points
        given their latitude/longitude in decimal degrees.

        Note: this treats degrees as flat Cartesian coordinates and
        does not account for Earth's curvature. It is only a reasonable
        approximation for points that are close together. Provided for
        comparison with the geodetic distance.

        Parameters
        ----------
        lat1, lon1, lat2, lon2 : float

        Returns
        -------
        float
            Distance in decimal degrees.
        """
        return np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

    def geodetic(self, lat1, lon1, lat2, lon2):
        """
        Compute the great-circle (geodetic) distance in kilometers
        between two points on Earth, using the Haversine formula.

        Parameters
        ----------
        lat1, lon1, lat2, lon2 : float

        Returns
        -------
        float
            Distance in kilometers.
        """
        lat1_r, lon1_r, lat2_r, lon2_r = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2_r - lat1_r
        dlon = lon2_r - lon1_r

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))

        return self.EARTH_RADIUS_KM * c

    def _distance_fn(self, method):
        if method == 'euclidean':
            return self.euclidean
        elif method == 'geodetic':
            return self.geodetic
        raise ValueError("method must be 'euclidean' or 'geodetic'")

    def nearest(self, station_id, n=3, method='geodetic'):
        """
        Find the n nearest stations to a given station.

        Parameters
        ----------
        station_id : int or str
            ID of the reference station.
        n : int
            Number of nearest stations to return.
        method : str
            Distance metric to use: 'euclidean' or 'geodetic'.

        Returns
        -------
        geopandas.GeoDataFrame
            The n nearest stations, with an added 'distance' column
            (in degrees for 'euclidean', in km for 'geodetic').
        """
        distance_fn = self._distance_fn(method)

        target_rows = self.stations[self.stations[self.id_col] == station_id]
        if target_rows.empty:
            raise ValueError(f"Station ID '{station_id}' not found.")
        target = target_rows.iloc[0]

        others = self.stations[self.stations[self.id_col] != station_id].copy()
        others['distance'] = others.geometry.apply(
            lambda p: distance_fn(target.geometry.y, target.geometry.x, p.y, p.x)
        )

        return others.nsmallest(n, 'distance')