# function(s) for plotting heatmap

import matplotlib.pyplot as plt
from matplotlib import transforms
import contextily as ctx
import geopandas as gpd
import numpy as np
from src.utils import load_bike_crash_data, prepare_crash_geodata

# Get global sizes for map, so map does not change when changing filters
_df_all = load_bike_crash_data()
_gdf_all = prepare_crash_geodata(_df_all)
FULL_BOUNDS = _gdf_all.total_bounds


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

    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_title("Bike Crashes in Chapel Hill (2007–2018)", fontsize=14)
    plt.tight_layout()
    return fig, ax


def plot_crash_hexbin(
    gdf_web: gpd.GeoDataFrame,
    basemap_style: str = "gray",
    gridsize: int = 40,
    ax=None,
):
    """Plot a hexbin density heatmap of crashes on an Esri basemap."""
    import numpy as np
    from scipy.spatial import cKDTree
    from collections import Counter

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    else:
        fig = ax.figure

    x = gdf_web.geometry.x
    y = gdf_web.geometry.y

    # Empty filtered dataset --------------------------------
    if gdf_web.empty or gdf_web.geometry.is_empty.all():
        xmin, ymin, xmax, ymax = FULL_BOUNDS
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ctx.add_basemap(ax, source=_get_basemap_source(basemap_style))

        for t in list(ax.texts):
            t.remove()

        ax.text(
            0.5, 0.5, "No data for selected filters",
            ha="center", va="center", fontsize=12, color="red",
            transform=ax.transAxes,
        )
        ax.set_frame_on(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        return fig, ax
    # ---------------------------------------------------------------

    xmin, ymin, xmax, ymax = FULL_BOUNDS

    # Plot hexbin
    hb = ax.hexbin(
        x,
        y,
        gridsize=gridsize,
        mincnt=1,
        alpha=0.4,
        extent=(xmin, xmax, ymin, ymax),
    )

    # fix hexbin stretch
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")

    # Add map background
    ctx.add_basemap(ax, source=_get_basemap_source(basemap_style))

    # remove contextily text
    for t in list(ax.texts):
        t.remove()

    # hide axis lines
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.set_title("Bike Crash Density – Chapel Hill", fontsize=14)
    cb = fig.colorbar(
        hb,
        ax=ax,
        orientation="horizontal",
        label="Crash Count",
        pad=0.02,
    )

    fig.subplots_adjust(left=0.02, right=0.98, top=1, bottom=0.15)

    # Tooltip is slightly heuristic. Maps points to nearest hex centers.
    centers = hb.get_offsets()
    points = np.column_stack((x.to_numpy(), y.to_numpy()))
    codes = gdf_web["BikeInjury"].to_numpy() 

    tree = cKDTree(centers)

    n_hex = centers.shape[0]
    sev_per_hex = [Counter() for _ in range(n_hex)]
    _, assigned_bins = tree.query(points)

    for p_idx, bin_idx in enumerate(assigned_bins):
        sev_per_hex[bin_idx][codes[p_idx]] += 1

    annot = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(20, 20),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->"),
        zorder=50,
    )
    annot.set_visible(False)

    def update_hex_annot(i):
        """Update tooltip text/position when hovering hex i."""
        cx, cy = centers[i]
        annot.xy = (cx, cy)

        sev_counts = sev_per_hex[i]

        if not sev_counts:
            annot.set_visible(False)
            return

        # Flip tooltip to avoid going off-screen
        midpoint = (xmin + xmax) / 2
        if cx > midpoint:
            annot.set_ha("right")
            annot.set_position((-20, 20))
        else:
            annot.set_ha("left")
            annot.xytext = (20, 20)
            annot.set_position((20, 20))

        text = "Crash Severity Counts:\n" + "\n".join(
            f"{k}: {v}" for k, v in sev_counts.items()
        )
        annot.set_text(text)

    def hover(event):
        if not event.inaxes:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()
            return

        # Nearest hex to cursor
        dist, idx = tree.query([event.xdata, event.ydata])
        hex_size = (xmax - xmin) / gridsize

        if dist < hex_size:
            update_hex_annot(idx)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    return fig, ax

