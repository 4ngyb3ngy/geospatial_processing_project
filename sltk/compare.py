from sltk.loader import load_station_series
from sltk.analysis import SeaLevelAnalysis
import pandas as pd
import geopandas as gpd


def compare_stations(loader_metadata, station_ids, data_dir, filename_template='{id}.rlrdata.txt'):
    """
    Compute sea level trends for multiple stations and merge them
    with their geographic location into a single GeoDataFrame.

    Parameters
    ----------
    loader_metadata : StationLoader
        Instance already loaded with station metadata (positions).
    station_ids : list
        List of station IDs to include in the comparison.
    data_dir : str
        Directory containing the raw PSMSL station files.
    filename_template : str
        Template to build each station's filename from its ID.

    Returns
    -------
    geopandas.GeoDataFrame
        Station metadata (name, position) with added columns:
        'trend_mm_per_year', 'r_squared', 'p_value'.
    """
    results = []

    for station_id in station_ids:
        filepath = f"{data_dir}/{filename_template.format(id=station_id)}"
        try:
            series = load_station_series(filepath)
            analysis = SeaLevelAnalysis(series['sea_level_mm'])
            trend_info = analysis.compute_trend()
            results.append({
                'ID': station_id,
                'trend_mm_per_year': trend_info['trend_mm_per_year'],
                'r_squared': trend_info['r_squared'],
                'p_value': trend_info['p_value'],
            })
        except FileNotFoundError:
            print(f"Warning: no data file found for station ID {station_id}, skipping.")

    trends_df = pd.DataFrame(results)

    stations_subset = loader_metadata.get_station(station_ids)
    merged = stations_subset.merge(trends_df, on='ID')
    return gpd.GeoDataFrame(merged, geometry='geometry', crs=stations_subset.crs)
