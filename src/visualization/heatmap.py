# function(s) for plotting heatmap

import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
import contextily as ctx
import geopandas as gpd
import numpy as np
import pandas as pd
from src.utils import load_bike_crash_data, prepare_crash_geodata

# get global sizes for map, so map does not change when changing filters
_df_all = load_bike_crash_data()
_gdf_all = prepare_crash_geodata(_df_all)
FULL_BOUNDS = _gdf_all.total_bounds


def _get_basemap_source(style: str, dark_mode: bool = False):
    """Small helper to choose ArcGIS basemap."""
    # If dark mode is enabled, use dark basemap
    if dark_mode:
        return ctx.providers.CartoDB.DarkMatter
    
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
    dark_mode: bool = False,
):
    """Plot crash points on an Esri basemap."""
    fig, ax = plt.subplots(figsize=figsize)

    gdf_web.plot(ax=ax, markersize=5, alpha=0.5)

    ctx.add_basemap(ax, source=_get_basemap_source(basemap_style, dark_mode=dark_mode))

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
    dark_mode: bool = False,
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

    if gdf_web.empty or gdf_web.geometry.is_empty.all():
        xmin, ymin, xmax, ymax = FULL_BOUNDS
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ctx.add_basemap(ax, source=_get_basemap_source(basemap_style, dark_mode=dark_mode))

        for t in list(ax.texts):
            t.remove()

        # apply dark mode styling if enabled
        # always reset colors to ensure proper switching between modes
        if dark_mode:
            fig.patch.set_facecolor('#1a1a1a')
            ax.set_facecolor('#1a1a1a')
            text_color = '#ff6b6b'  # Lighter red for dark background
        else:
            # reset to light mode defaults
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            text_color = "red"

        ax.text(
            0.5, 0.5, "No data for selected filters",
            ha="center", va="center", fontsize=12, color=text_color,
            transform=ax.transAxes,
        )
        ax.set_frame_on(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        return fig, ax

    xmin, ymin, xmax, ymax = FULL_BOUNDS

    hexbin_cmap = cm.plasma
    # Plot hexbin
    hb = ax.hexbin(
        x,
        y,
        gridsize=gridsize,
        mincnt=1,
        alpha=0.4,
        extent=(xmin, xmax, ymin, ymax),
        cmap=hexbin_cmap,
    )

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")

    # Add map background
    ctx.add_basemap(ax, source=_get_basemap_source(basemap_style, dark_mode=dark_mode))

    # remove contextily text
    for t in list(ax.texts):
        t.remove()

    # hide axis lines
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # always reset colors for switching between modes
    if dark_mode:
        fig.patch.set_facecolor('#1a1a1a')  # Dark background for figure
        ax.set_facecolor('#1a1a1a')  # Dark background for axes
        title_color = 'white'
        label_color = 'white'
        tick_color = 'white'
    else:
        # reset to light mode defaults
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        title_color = 'black'
        label_color = 'black'
        tick_color = 'black'

    ax.set_title("Bike Crash Density – Chapel Hill", fontsize=14, color=title_color)
    cb = fig.colorbar(
        hb,
        ax=ax,
        orientation="horizontal",
        label="Crash Count",
        pad=0.05,
        shrink=0.95
    )
    cb.set_label("Crash Count", color=label_color)
    cb.ax.xaxis.set_tick_params(color=tick_color)
    cb.ax.xaxis.label.set_color(label_color)
    plt.setp(plt.getp(cb.ax.axes, 'xticklabels'), color=tick_color)

    fig.subplots_adjust(left=0.005, right=0.995, top=1, bottom=0.1)

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

        # Set tooltip background color based on dark mode
        tooltip_bg = '#2a2a2a' if dark_mode else 'w'
        tooltip_text_color = 'white' if dark_mode else 'black'
        annot = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(20, 20),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc=tooltip_bg, ec='gray' if dark_mode else 'black'),
        arrowprops=dict(arrowstyle="->", color='white' if dark_mode else 'black'),
        zorder=50,
        color=tooltip_text_color,
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

        # Flip tooltip to avoid going off-screen horizontally
        midpoint = (xmin + xmax) / 2
        if cx > midpoint:
            annot.set_ha("right")
            annot.set_position((-20, 20))
        else:
            annot.set_ha("left")
            annot.xytext = (20, 20)
            annot.set_position((20, 20))

        # Flip tooltip to avoid going off-screen vertically
        midpoint_y = (ymin + ymax) / 2
        if cy > midpoint_y:
            annot.set_va("top")
            annot.set_position((20, -20))
        else:
            annot.set_va("bottom")
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


def animate_crash_density_over_time(
    df: pd.DataFrame = None,
    basemap_style: str = "gray",
    gridsize: int = 40,
    year_col: str = "CrashYear",
    interval: int = 1000,
    figsize=(10, 10),
    save_path: str = None,
):

    df = load_bike_crash_data()
    df = df[df[year_col].notna()].copy()
    
    years = sorted(df[year_col].unique())
    years = [int(y) for y in years if pd.notna(y)]

    # prepare GeoDataFrame for all data to get consistent bounds
    gdf_all = prepare_crash_geodata(df)
    xmin, ymin, xmax, ymax = gdf_all.total_bounds
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    # store data by year
    gdf_by_year = {}
    for year in years:
        df_year = df[df[year_col] == year].copy()
        if len(df_year) > 0:
            gdf_year = prepare_crash_geodata(df_year)
            gdf_by_year[year] = gdf_year
            print(f"Year {year}: {len(gdf_year)} crashes with valid coordinates")
        else:
            gdf_by_year[year] = gpd.GeoDataFrame(geometry=[], crs="EPSG:3857")
            print(f"Year {year}: 0 crashes")
    
    # initialize empty hexbin and colorbar
    hb = None
    cb = None
    
    basemap_source = _get_basemap_source(basemap_style)
    
    def animate(frame):
        """Update function for animation"""
        nonlocal hb, cb
        
        year = years[frame]
        
        if cb is not None:
            try:
                cb.remove()
            except (AttributeError, ValueError):
                pass  # colorbar already removed or doesn't exist
        
        ax.clear()
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_aspect("equal")
        ax.set_frame_on(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        # add basemap
        ctx.add_basemap(ax, source=basemap_source, crs="EPSG:3857", zorder=0)
        
        # remove contextily text
        for t in list(ax.texts):
            if t.get_text() == "" or "contextily" in str(t).lower():
                t.remove()
        
        # data for this year
        gdf_year = gdf_by_year[year]
        
        title_text = ax.text(
            0.5, 0.95,
            f"Bike Crash Density - Year {year}\n({len(gdf_year)} crashes)",
            transform=ax.transAxes,
            ha="center",
            fontsize=16,
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8),
            zorder=100
        )
        
        # plot hexbin for this year
        if not gdf_year.empty and not gdf_year.geometry.is_empty.all():
            x = gdf_year.geometry.x
            y = gdf_year.geometry.y
            
            hb = ax.hexbin(
                x,
                y,
                gridsize=gridsize,
                mincnt=1,
                alpha=0.6,
                extent=(xmin, xmax, ymin, ymax),
                cmap="YlOrRd",  # Yellow-Orange-Red colormap
                zorder=10
            )
            
            # add colorbar
            cb = fig.colorbar(
                hb,
                ax=ax,
                orientation="horizontal",
                label="Crash Count",
                pad=0.05,
                shrink=0.95
            )
        else:
            # no data for this year - create empty hexbin to maintain structure
            hb = ax.hexbin(
                [],
                [],
                gridsize=gridsize,
                mincnt=1,
                alpha=0.6,
                extent=(xmin, xmax, ymin, ymax),
                cmap="YlOrRd",
                zorder=10
            )
            cb = fig.colorbar(
                hb,
                ax=ax,
                orientation="horizontal",
                label="Crash Count",
                pad=0.05,
                shrink=0.95
            )
        
        fig.subplots_adjust(left=0.005, right=0.995, top=0.95, bottom=0.1)
        fig.canvas.draw_idle()
        
        return hb, title_text
    
    animate(0)
    
    anim = FuncAnimation(
        fig,
        animate,
        frames=len(years),
        interval=interval,
        repeat=True,
        blit=False  # blit=False because we're removing/adding elements
    )
    
    # save animation if path flagged
    if save_path:
        print(f"Saving animation to {save_path}...")
        anim.save(save_path, writer="pillow", fps=1)
        print("Animation saved!")
    
    return fig, anim
