"""
SLTK: Sea Level Tool Kit

A Python library for loading, analyzing, and comparing sea level
data from PSMSL tide gauge stations.
"""

from sltk.loader import load_station_series
from sltk.loader_metadata import StationLoader
from sltk.analysis import SeaLevelAnalysis
from sltk.geometry import p_in_poly, point_in_region, filter_stations_by_region
from sltk.distances import Distances
from sltk.compare import compare_stations

__version__ = "0.1.0"

__all__ = [
    "load_station_series",
    "StationLoader",
    "SeaLevelAnalysis",
    "p_in_poly",
    "point_in_region",
    "filter_stations_by_region",
    "Distances",
    "compare_stations",
]
