# function(s) for plotting heatmap

import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd

def _get_basemap_source(style: str):
    """Small helper to choose ArcGIS basemap."""
    style = style.lower()
    if style in ("street", "streets"):
        return ctx.providers.Esri.WorldStreetMap
    if style in ("gray", "grey", "lightgray", "light"):
        return ctx.providers.Esri.WorldGrayCanvas
    if style in ("topo", "topographic"):
        return ctx.providers.Esri.WorldTopoMap
    return ctx.providers.Esri.WorldStreetMap  # default

def plot_crash_points(
    gdf_web: gpd.GeoDataFrame,
    basemap_style: str = "street",
    figsize=(8, 8),
):
    """Plot crash points on an Esri basemap."""
    fig, ax = plt.subplots(figsize=figsize)

    gdf_web.plot(ax=ax, markersize=5, alpha=0.5)

    ctx.add_basemap(ax, source=_get_basemap_source(basemap_style))

    ax.set_axis_off()
    ax.set_title("Bike Crashes in Chapel Hill (2007–2018)", fontsize=14)
    plt.tight_layout()
    return fig, ax

def plot_crash_hexbin(
    gdf_web: gpd.GeoDataFrame,
    basemap_style: str = "gray",
    gridsize: int = 40,
    figsize=(8, 8),
):
    """Plot a hexbin density heatmap of crashes on an Esri basemap."""
    import numpy as np  # local import if you prefer

    fig, ax = plt.subplots(figsize=figsize)
    x = gdf_web.geometry.x
    y = gdf_web.geometry.y

    hb = ax.hexbin(
        x, y,
        gridsize=gridsize,
        mincnt=1,
        alpha=0.7,
    )

    ctx.add_basemap(ax, source=_get_basemap_source(basemap_style))

    ax.set_axis_off()
    ax.set_title("Bike Crash Density – Chapel Hill", fontsize=14)

    cb = fig.colorbar(hb, ax=ax, label="Crash Count")
    plt.tight_layout()
    return fig, ax
