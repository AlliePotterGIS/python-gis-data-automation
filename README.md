
# Storm Response GIS

## Severe Weather & Tree-Impact Analysis
![2025 Missouri Storm-Related Tree Impacts](images/missouri_tree_impacts_2025.jpg)
This project explores how GIS and Python can support storm-response operations by identifying and mapping severe-weather events associated with reported tree impacts.

The project uses publicly available NOAA Storm Events data and U.S. Census Bureau geographic data to create a reproducible workflow for identifying, processing, mapping, and analyzing storm-related tree impacts.

## Project Question

**Where were tree-related wind and tornado impacts documented in Missouri during 2025, and what geographic patterns can be identified from those events?**

## Current Results

The initial analysis processed **72,360 NOAA Storm Events records** from 2025.

The workflow identified:

- **2,757** storm events in Missouri
- **1,107** Missouri wind-related events
- **711** events with tree-related terminology in the NOAA event narrative
- **683** tree-impact events with usable geographic coordinates
- **682** events successfully spatially matched to Missouri counties

The most frequently represented counties in the spatial analysis were:

| County | Tree-Impact Events |
|---|---:|
| Jackson | 69 |
| Greene | 58 |
| Christian | 41 |
| Clay | 23 |
| St. Louis | 20 |

These values represent NOAA event records meeting the project's classification criteria and should not be interpreted as insurance claim counts or individual damaged properties.

## Methodology

### 1. Data Acquisition

NOAA Storm Events bulk data for 2025 was used as the primary event dataset.

### 2. Geographic Filtering

The national dataset was filtered to records where:

`STATE = MISSOURI`

This reduced the dataset from **72,360** national records to **2,757** Missouri records.

### 3. Event-Type Filtering

The analysis selected storm types with the potential to produce tree impacts:

- Thunderstorm Wind
- Tornado
- High Wind
- Strong Wind

This produced **1,107** candidate events.

### 4. Tree-Impact Classification

NOAA's `EVENT_NARRATIVE` field was searched for tree-related terminology including:

- tree / trees
- branch / branches
- limb / limbs
- trunk / trunks

Events containing at least one of these terms were classified with:

`TREE_IMPACT = True`

This identified **711** events with tree-related terminology.

### 5. Coordinate Quality Control

Records without `BEGIN_LAT` or `BEGIN_LON` coordinates were excluded from point mapping.

Of the 711 classified events:

- **683** contained usable starting coordinates
- **28** lacked usable starting coordinates

### 6. Spatial Data Creation

GeoPandas was used to convert the filtered records into point geometries using:

`BEGIN_LON` and `BEGIN_LAT`

The resulting GeoDataFrame uses:

`EPSG:4326 — WGS 84`

The processed spatial dataset was exported as a GeoPackage for use in desktop GIS software.

### 7. County Spatial Analysis

Missouri county boundaries from the U.S. Census Bureau TIGERweb service were used for county-level analysis.

ArcGIS Pro Spatial Join was used to aggregate the NOAA point features to Missouri counties.

Of the **683** geocoded events, **682** intersected a Missouri county polygon.

One tornado event located along the Missouri state border did not intersect a Missouri county polygon and was retained in the source dataset but excluded from county aggregation.

This record was:

- NOAA Event ID: `1255585`
- Event Type: Tornado
- NOAA County/Zone: Jasper
- Latitude: `37.1297`
- Longitude: `-94.618`

No attempt was made to manually move or alter the source coordinates.

## Reproducible Workflow

```text
NOAA Storm Events CSV
        ↓
Filter to Missouri
        ↓
Select Wind-Related Events
        ↓
Search Event Narratives
        ↓
Identify Tree-Impact Records
        ↓
Remove Records Without Coordinates
        ↓
Create GeoPandas Point Geometry
        ↓
Export GeoPackage
        ↓
Spatial Join to Missouri Counties
        ↓
Map & Analyze Geographic Patterns
```

## Technologies

- Python
- pandas
- GeoPandas
- ArcGIS Pro
- NOAA Storm Events Database
- U.S. Census Bureau TIGERweb
- GeoPackage
- Git / GitHub

## Repository Structure

```text
storm-response-gis/
│
├── README.md
├── data/
│   └── raw/
└── src/
    └── process_storm_data.py
```

### `src/process_storm_data.py`

The Python processing script automatically:

1. Locates the NOAA Storm Events CSV
2. Loads the source data with pandas
3. Filters records to Missouri
4. Selects wind-related event types
5. Searches NOAA narratives for tree-impact terminology
6. Removes records without usable coordinates
7. Creates GIS point geometries with GeoPandas
8. Assigns the WGS 84 coordinate reference system
9. Exports the processed data to a GeoPackage

## Data Quality & Limitations

This analysis identifies NOAA event narratives containing selected tree-related terminology. A positive classification indicates that the narrative contains those terms; it does **not** necessarily indicate damage to an insured property or represent an individual insurance claim.

NOAA property-damage values also contain missing observations. Missing damage estimates are preserved as unknown rather than being interpreted as zero damage.

Event coordinates represent locations reported in the NOAA Storm Events dataset and may not represent the full geographic extent of an event.

## Next Steps

Planned development includes:

- Add Census housing exposure data
- Calculate county-level exposure metrics
- Incorporate reported property-damage estimates
- Investigate tree-canopy or land-cover data
- Develop a transparent storm-response priority index
- Create publication-quality maps
- Expand the analysis beyond a single year
- Develop an interactive web GIS application

## Disclaimer

This is an independent GIS portfolio project created for educational and professional-development purposes.

The project uses publicly available government data and does not contain proprietary company information, customer information, insurance claims, contractor information, or other confidential data.

## Author

**Allie Potter**  
GIS Analyst | Geospatial Developer
