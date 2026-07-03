import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

class StationLoader:
    def __init__(self, filepath):
        """
        Parameters
        ----------
        filepath : str
            Path to the CSV/Excel file with station metadata.
            Expected columns: 'Name', 'Coastline', 'ID', 'Lat', 'Lon'.
        """
        self.filepath = filepath
        self.metadata = self.load_stations_metadata()

    def load_stations_metadata(self):
        """
        Load station metadata (name, ID, coordinates, CoastLine etc.) and convert to a GeoDataFrame.

        Returns
        -------
        geopandas.GeoDataFrame
            Station metadata with a 'geometry' column of Point objects (EPSG:4326).
        """
        df = pd.read_csv(self.filepath, sep=';', header=0, encoding='latin-1')
        geometry = [Point(lon, lat) for lon, lat in zip(df['Lon'], df['Lat'])] #touples of the coordinates
        # nb! in shapley we've longitude -> x and latitude -> y
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        return gdf

    def get_station(self, station_id):
        """
        Return metadata for one or more stations that are passed as a list.

        Parameters
        ----------
        station_id : int
            The ID (or list of IDs) of the station(s) to retrieve.

        Returns
        -------
            geopandas.GeoDataFrame
            Metadata for the station(s) matching the given ID(s).
        """
        if not isinstance(station_id, list):
            station_id = [station_id]
        return self.metadata[self.metadata['ID'].isin(station_id)]