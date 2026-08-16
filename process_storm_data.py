import pandas as pd
import geopandas as gpd
from pathlib import Path

# Define project folders
project_folder = Path.home() / "OneDrive" / "Documents" / "storm-response-gis"
raw_folder = project_folder / "data" / "raw"
processed_folder = project_folder / "data" / "processed"

# Find the NOAA Storm Events CSV
csv_files = list(raw_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {raw_folder}")

input_file = csv_files[0]

# Load the NOAA Storm Events data
df = pd.read_csv(input_file)

# Filter to Missouri events
missouri = df[df["STATE"] == "MISSOURI"].copy()

print(f"Missouri events: {len(missouri):,}")

# Keep wind-related storm types relevant to potential tree impacts
tree_event_types = [
    "Thunderstorm Wind",
    "Tornado",
    "High Wind",
    "Strong Wind",
]

tree_events = missouri[missouri["EVENT_TYPE"].isin(tree_event_types)].copy()

print(f"Wind-related Missouri events: {len(tree_events):,}")

# Identify events whose NOAA narrative mentions tree-related impacts
tree_pattern = (
    r"\btree\b|\btrees\b|"
    r"\bbranch\b|\bbranches\b|"
    r"\blimb\b|\blimbs\b|"
    r"\btrunk\b|\btrunks\b"
)

tree_events["TREE_IMPACT"] = (
    tree_events["EVENT_NARRATIVE"]
    .fillna("")
    .str.contains(tree_pattern, case=False, regex=True)
)

tree_impacts = tree_events[tree_events["TREE_IMPACT"]].copy()

print(f"Tree-impact events: {len(tree_impacts):,}")

# Keep only events with valid starting coordinates
spatial_events = tree_impacts.dropna(
    subset=["BEGIN_LAT", "BEGIN_LON"]
).copy()

print(f"Mappable tree-impact events: {len(spatial_events):,}")

# Convert the filtered records to a GeoDataFrame
spatial_events = gpd.GeoDataFrame(
    spatial_events,
    geometry=gpd.points_from_xy(
        spatial_events["BEGIN_LON"],
        spatial_events["BEGIN_LAT"]
    ),
    crs="EPSG:4326"
)

print(f"GeoDataFrame created with {len(spatial_events):,} features")

# Ensure the processed-data folder exists
processed_folder.mkdir(parents=True, exist_ok=True)

# Export the spatial dataset as a GeoPackage
output_file = processed_folder / "missouri_tree_impacts_2025.gpkg"

spatial_events.to_file(
    output_file,
    layer="tree_impacts",
    driver="GPKG"
)

print(f"Saved output to: {output_file}")


