# SLTK: Sea Level Tool Kit

SLTK is a Python library designed to monitor and analyze sea level data from PSMSL (Permanent Service for Mean Sea Level) tide gauge stations. The library provides tools to load and clean raw station records, compute long-term trends and seasonal patterns, perform spatial queries on station locations, and compare sea level behaviour across multiple stations.

The current implementation focuses on **vector** geospatial data (station locations as points) combined with **time series analysis** of sea level records. A natural future extension — not yet implemented — would be to organize multi-station records into a true `time × station` **datacube** (e.g. with `xarray`), and to extend the library to support gridded satellite data from **CMEMS** (Copernicus Marine Environment Monitoring Service). Anyone interested in developing this direction is welcome to build on the existing functions, adapting the CMEMS data format to the structure used for PSMSL data in this library.

## Features

The library provides tools to:

* **Load and clean** raw PSMSL monthly sea level records, handling missing-value codes and converting decimal-year timestamps to proper dates (`sltk.loader`)
* **Load and manage station metadata** (name, coordinates, country) as a `geopandas.GeoDataFrame`, with lookup by one or more station IDs (`sltk.loader_metadata`)
* **Compute long-term sea level trends** (mm/year) via linear regression, and **extract seasonal cycles** (average sea level by calendar month) (`sltk.analysis`)
* **Test whether a station falls within a country's boundary**, using a **custom implementation** of the even–odd (ray-casting) point-in-polygon algorithm — not a call to a pre-built spatial predicate (`sltk.geometry`)
* **Compute distances between stations**, using either a simple Euclidean approximation or the geodetic (Haversine great-circle) distance, and **find the nearest stations** to a given one (`sltk.distances`)
* **Compare trends across multiple stations**, merging computed trends with station locations into a single spatial dataset ready for mapping (`sltk.compare`)

## Data

### Sea level records

Sea level data comes from the [PSMSL](https://www.psmsl.org/data/obtaining/) RLR (Revised Local Reference) **monthly** dataset. Each station is a semicolon-separated `.rlrdata.txt` file with the format:

```
date_decimal; sea_level_mm; interpolated_flag; missing_days
```

Missing months are coded as `-99999` in the raw file; `load_station_series` converts these to `NaN`. Dates are given as decimal years following PSMSL's mid-month convention and are converted to proper `datetime` objects (day fixed to the 15th, since the underlying data represents a monthly average, not a specific day).

### Station metadata

Station metadata (name, ID, latitude/longitude, country, etc.) is provided in `data/metadata_stations.csv`, sourced from the [PSMSL station catalogue](https://www.psmsl.org/data/obtaining/).

### Country boundaries

Country boundaries used for the point-in-polygon spatial queries come from [Natural Earth](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/) (110m resolution, `SOV_A3` ISO-3166 alpha-3 country codes).

### Station selection

The example analysis in this repository focuses on **seven Italian coastal stations**, chosen to cover different surrounding seas (Adriatic, Ionian, Tyrrhenian, Ligurian):

| Station | Sea | PSMSL ID |
|---|---|---|
| Trieste | Adriatic (north) | 154 |
| Ancona II | Adriatic (centre) | 2098 |
| Bari | Adriatic (south) | 2075 |
| Taranto II | Ionian | 2095 |
| Reggio Calabria II | Tyrrhenian / Strait | 2142 |
| Palermo II | Tyrrhenian (Sicily) | 2093 |
| Genova II | Ligurian | 2090 |

Trieste has an exceptionally long record (1875–2024) and is used separately as a long-term case study, while the other six stations (2001–2025) are used for the modern multi-station comparison. **Venezia (Punta della Salute)** was evaluated but excluded from the multi-station comparison: its record ends around 2000, leaving essentially no temporal overlap with the other modern stations.

## Installation

Clone the repository and install the package (editable mode is recommended during development):

```bash
git clone <repository-url>
cd sltk
pip install -e .
```

Dependencies (see `pyproject.toml` / `requirements.txt`): `pandas`, `numpy`, `geopandas`, `shapely`, `scipy`, `matplotlib`.

## Quick usage example

```python
from sltk.loader import load_station_series
from sltk.loader_metadata import StationLoader
from sltk.analysis import SeaLevelAnalysis
from sltk.distances import Distances
from sltk.compare import compare_stations

# Load a single station's cleaned time series
trieste = load_station_series("data/stations/154.rlrdata.txt")

# Compute its long-term trend and seasonal cycle
analysis = SeaLevelAnalysis(trieste["sea_level_mm"])
trend = analysis.compute_trend()
seasonal = analysis.seasonal_cycle()
print(trend)  # {'trend_mm_per_year': 1.35, 'r_squared': 0.29, 'p_value': 4e-124}

# Load station metadata and find the nearest stations to Trieste
loader_metadata = StationLoader("data/metadata_stations.csv")
dist = Distances(loader_metadata.metadata, id_col="ID")
nearest = dist.nearest(station_id=154, n=3, method="geodetic")

# Compare trends across multiple stations, with their spatial location
station_ids = [154, 2098, 2075, 2095, 2142, 2093, 2090]
comparison = compare_stations(loader_metadata, station_ids, data_dir="data/stations")
```

## Testing

Unit tests are provided under `tests/`, covering all modules of the library (loading, metadata, analysis, geometry, distances, and comparison). Run them with:

```bash
python -m pytest tests/ -v
```

## Project structure

```
sltk/
├── sltk/
│   ├── __init__.py
│   ├── loader.py            # load_station_series
│   ├── loader_metadata.py   # StationLoader
│   ├── analysis.py          # SeaLevelAnalysis
│   ├── geometry.py          # custom point-in-polygon
│   ├── distances.py         # Distances
│   └── compare.py           # compare_stations
├── data/
│   ├── metadata_stations.csv
│   ├── stations/             # raw PSMSL .rlrdata.txt files
│   └── boundaries/           # Natural Earth country boundaries
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Notes and limitations

* The point-in-polygon check in `sltk.geometry` is implemented from scratch (even–odd ray-casting algorithm), rather than relying on `shapely`'s built-in spatial predicates, and has been validated against `shapely.contains()`.
* The Euclidean distance in `sltk.distances` is provided mainly for comparison; it treats latitude/longitude as flat coordinates and does not account for Earth's curvature. The geodetic (Haversine) distance should be used for any real-world distance measurement.
* Trend estimates for the six modern stations (2001–2025) are based on a comparatively short record and should be interpreted with caution relative to Trieste's 149-year series.

---

This library was developed as a project for the Geospatial Processing course, academic year 2025/2026.
