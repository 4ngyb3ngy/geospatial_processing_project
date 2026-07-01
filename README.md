#SLTK: Sea Level Tool Kit
SLTK is a Python library designed to monitor and analyze sea level data from PSMSL (Permanent Service for Mean Sea Level) tide gauge stations. The library organizes records from multiple stations into a datacube-style structure (time × station), enabling trend detection, seasonal pattern analysis, and comparison across locations.
Future extensions could include support for CMEMS gridded satellite data. Anyone interested in developing this direction is welcome to build on the existing functions, adapting the CMEMS data format to match the structure used for PSMSL data in this library.

The library provides tools to:
* Load and clean sea level records from PSMSL station files
* Organize multi-station data into a time × station datacube (xarray)
* Compute long-term sea level trends (mm/year) via linear regression
* Extract seasonal cycles (average monthly variation)
* Compare trends across multiple stations, including their spatial location
