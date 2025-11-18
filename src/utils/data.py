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

    # rough bounds of chapel hill, nc; tweak if wrong
    lat_min, lat_max = 35.85, 36.10
    lon_min, lon_max = -79.15, -78.90
    df = df[
        df[lat_col].between(lat_min, lat_max)
        & df[lon_col].between(lon_min, lon_max)
    ]

    # create GeoDataFrame in WGS84
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326",
    )

    # reproject to Web Mercator for tile basemaps
    gdf_web = gdf.to_crs(epsg=3857)
    return gdf_web