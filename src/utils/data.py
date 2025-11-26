# functions for loading and manipulating data
import kagglehub
import pandas as pd
import os

import pandas as pd
import geopandas as gpd

def load_bike_crash_data() -> pd.DataFrame:
    path = kagglehub.dataset_download("adityadesai13/11000-bike-crash-data")

    # Find the first CSV inside the downloaded directory
    for f in os.listdir(path):
        if f.endswith(".csv"):
            csv_path = os.path.join(path, f)
            break
    else:
        raise FileNotFoundError("No CSV file found in downloaded dataset")

    df = pd.read_csv(csv_path)
    return df

def prepare_crash_geodata(
    df: pd.DataFrame,
    lat_col: str = "Latitude",
    lon_col: str = "Longitude",
) -> gpd.GeoDataFrame:
    """
    Take raw crash dataframe and return a GeoDataFrame in Web Mercator (EPSG:3857) for mapping.
    """

    df = df[df[lat_col].notna() & df[lon_col].notna()].copy()

    len_raw = len(df)           # len of df before prepare_crash_geodata

    # rough bounds of chapel hill, nc; tweak if wrong
    # lat_min, lat_max = 35.85, 36.10
    # lon_min, lon_max = -79.15, -78.90

    # lat_min, lat_max = df["Latitude"].quantile([0.01, 0.99])
    # lon_min, lon_max = df["Longitude"].quantile([0.01, 0.99])

    # use full range of lat/lon in df
    lat_min, lat_max = 33.5, 36.7
    lon_min, lon_max = -84.3, -75.2

    df = df[
        df[lat_col].between(lat_min, lat_max)
        & df[lon_col].between(lon_min, lon_max)
    ]

    len_clean = len(df)         # len of df after filtering lat/lon
    print(len_raw, len_clean)

    # create GeoDataFrame in WGS84
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326",
    )

    # reproject to Web Mercator for tile basemaps
    gdf_web = gdf.to_crs(epsg=3857)
    return gdf_web

def filter_data(df: pd.DataFrame, column_name: str, choice: str) -> pd.DataFrame:
    """
    Takes a dataframe, a column name to filter, and a choice to filter it on (categorical choice). Returns the filtered dataframe.
    """
    df_filtered = df.copy()
    # Any choice doesn't need to filter
    yes_no_choices = ["CrashAlcoh", "HitRun"]
    if choice == "Any":
        return df_filtered

    # For Columns where the selection is baked into the choice window. Ex:LightCond, BikePos, TraffCntrl, SpeedLimit
    if column_name not in yes_no_choices:
        df_filtered = df_filtered[df_filtered[column_name] == choice]
    # For all columns whose choices are any, yes, no Ex:CrashAlcoh, HitRun
    elif choice == "Yes":
        df_filtered = df_filtered[df_filtered[column_name] == "Yes"]
    elif choice == "No":
        df_filtered = df_filtered[df_filtered[column_name] == "No"]

    return df_filtered