import pandas as pd
import geopandas as gpd
from pathlib import Path
import requests 

# Define project folders
project_folder = Path.home() / "OneDrive" / "Documents" / "storm-response-gis"
raw_folder = project_folder / "data" / "raw"
processed_folder = project_folder / "data" / "processed"

# Read the Census API key from a local file
census_key_file = project_folder / "census_api_key.txt"
census_api_key = census_key_file.read_text().strip()

# ------------------------------------------------------------
# NOAA Storm Events processing
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Census housing exposure data
# ------------------------------------------------------------

# Request 2020 Census housing-unit data for Missouri counties
census_url = "https://api.census.gov/data/2020/dec/dhc"

census_params = {
    "get": "NAME,H1_001N",
    "for": "county:*",
    "in": "state:29",
    "key": census_api_key,
}

response = requests.get(census_url, params=census_params)
response.raise_for_status()

housing_data = response.json()

print(f"Census county records retrieved: {len(housing_data) - 1}")
# Convert Census API response to a pandas DataFrame
housing_df = pd.DataFrame(
    housing_data[1:],
    columns=housing_data[0]
)

# Convert housing-unit counts from text to integers
housing_df["H1_001N"] = housing_df["H1_001N"].astype(int)

print(housing_df.head())

# Create a simplified county name field
housing_df["COUNTY_NAME"] = (
    housing_df["NAME"]
    .str.replace(" County, Missouri", "", regex=False)
    .str.replace(" city, Missouri", "", regex=False)
)

print(housing_df[["NAME", "COUNTY_NAME", "H1_001N"]].head(10))

# Create the 5-digit county GEOID from state and county FIPS codes
housing_df["GEOID"] = (
    housing_df["state"].astype(str).str.zfill(2)
    + housing_df["county"].astype(str).str.zfill(3)
)

# Ensure GEOID is stored as text in pandas
housing_df["GEOID"] = housing_df["GEOID"].astype(str)

print(housing_df[["COUNTY_NAME", "GEOID", "H1_001N"]].head(10))

# Save cleaned Census housing data
housing_output = processed_folder / "missouri_county_housing_2020.csv"

housing_df.to_csv(housing_output, index=False)

print(f"Saved Census housing data to: {housing_output}")

# Save cleaned Census housing data
housing_output = processed_folder / "missouri_county_housing_2020.csv"

housing_df.to_csv(housing_output, index=False)

print(f"Saved Census housing data to: {housing_output}")


