import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import re
import matplotlib.cm as cm

def adjusted_colormap(cmap, minval=0, maxval=1.0, n=100):
        new_cmap = mcolors.LinearSegmentedColormap.from_list(
            f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
            cmap(np.linspace(minval, maxval, n))
        )
        return new_cmap

SEVERITY_ORDER = [
    "O: No Injury",
    "C: Possible Injury",
    "B: Suspected Minor Injury",
    "A: Suspected Serious Injury",
    "K: Killed"
]

SEVERITY_COLORS = {
    "O: No Injury": "#7fc97f",
    "C: Possible Injury": "#beaed4",
    "B: Suspected Minor Injury": "#fdc086",
    "A: Suspected Serious Injury": "#f0027f",
    "K: Killed": "#000000"
}

VALID_SURFACES = [
    "Coarse Asphalt",
    "Concrete",
    "Gravel",
    "Grooved Concrete",
    "Other",
    "Sand",
    "Smooth Asphalt",
    "Soil"
]

BAD_VALUES = {"nan", "NaN", "", " ", "NONE", "None", "UNKNOWN", "Missing"}


def plot_severity_matrix(df, ax=None, row_var="RdSurface", col_var="SpeedLimit"):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    df = df.copy()

    df = df.dropna(subset=[row_var, col_var])

    df[row_var] = df[row_var].astype(str).str.strip()
    df[col_var] = df[col_var].astype(str).str.strip()

    df = df[~df[row_var].isin(BAD_VALUES)]
    df = df[~df[col_var].isin(BAD_VALUES)]

    df = df[df[row_var].isin(VALID_SURFACES)]

    surface_counts = df[row_var].value_counts()
    valid_surfaces_with_enough_data = surface_counts[surface_counts >= 20].index.tolist()
    df = df[df[row_var].isin(valid_surfaces_with_enough_data)]

    row_cats = [s for s in VALID_SURFACES if s in df[row_var].unique()]
    row_cats.append("Overall")

    def sort_speed_key(value):
        """Sort key for speed limits: numeric values first (ascending), then non-numeric"""
        value_str = str(value).strip().lower()
        
        if value_str in ["unknown", "unk", "n/a", "na", "none", ""]:
            return (1, float('inf'), value_str)
        
        try:
            numbers = re.findall(r'\d+', value_str)
            if numbers:
                num_value = int(numbers[0])
                return (0, num_value, value_str)
        except:
            pass
        
        return (0, float('inf'), value_str)
    
    col_cats = sorted(df[col_var].unique(), key=sort_speed_key)

    nrows, ncols = len(row_cats), len(col_cats)
    fig.clear()
    
    if nrows == 0 or ncols == 0:
        ax = fig.add_subplot(1, 1, 1)
        ax.text(0.5, 0.5, "No data available\nfor the selected filters.\n\nTry selecting a different\nRoadway Feature or\ncheck your data filters.",
                ha="center", va="center", fontsize=12, 
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        return fig
    
    axs = fig.subplots(nrows, ncols, sharex=False, sharey=False)

    if nrows == 1 and ncols == 1:
        axs = np.array([[axs]])
    elif nrows == 1:
        axs = np.array([axs])
    elif ncols == 1:
        axs = axs.reshape(nrows, 1)
    else:
        axs = np.array(axs)

    row_max_counts = {}
    for i, surface in enumerate(row_cats):
        row_max = 0
        for j, speed in enumerate(col_cats):
            if surface == "Overall":
                subdf = df[df[col_var] == speed]
            else:
                subdf = df[(df[row_var] == surface) & (df[col_var] == speed)]
            if not subdf.empty:
                counts = subdf["BikeInjury"].value_counts()
                if len(counts) > 0:
                    max_count = int(counts.max())
                    row_max = max(row_max, max_count)
        row_max_counts[i] = max(row_max, 1)

    for i in range(nrows):
        max_count = row_max_counts[i]
        y_max = max_count * 1.1
        if y_max > 10:
            y_max = np.ceil(y_max / 10) * 10
        else:
            y_max = np.ceil(y_max)
        
        if ncols > 1:
            for j in range(1, ncols):
                axs[i][j].sharey(axs[i][0])
        
        axs[i][0].set_ylim(0, y_max)

    for i, surface in enumerate(row_cats):
        for j, speed in enumerate(col_cats):

            cell_ax = axs[i][j]

            if surface == "Overall":
                subdf = df[df[col_var] == speed]
            else:
                subdf = df[(df[row_var] == surface) & (df[col_var] == speed)]

            if i == 0:
                cell_ax.set_title(speed, fontsize=10)

            if j > 0:
                cell_ax.tick_params(left=True, labelleft=False)
            else:
                cell_ax.tick_params(left=True, labelleft=True)

            if subdf.empty:
                cell_ax.text(0.5, 0.5, "No data",
                             ha="center", va="center", fontsize=8)
                cell_ax.set_xticks([])
                if j > 0:
                    cell_ax.tick_params(left=True, labelleft=False)
                continue

            counts = subdf["BikeInjury"].value_counts()
            count_values = [counts.get(sev, 0) for sev in SEVERITY_ORDER]

            x = np.arange(len(SEVERITY_ORDER))

            cmap = adjusted_colormap(cm.YlOrRd, 0.3)
            norm = mcolors.Normalize(vmin=0, vmax=len(SEVERITY_ORDER) - 1)
            colors = [cmap(norm(i)) for i in range(len(SEVERITY_ORDER))]

            cell_ax.bar(
                x,
                count_values,
                color=colors,
                width=0.7
            )

            if i == nrows - 1:
                cell_ax.set_xticks(x)
                cell_ax.set_xticklabels(
                    ["No", "Poss", "Minor", "Serious", "Kill"],
                    fontsize=6,
                    rotation=45
                )
            else:
                cell_ax.set_xticks([])
                cell_ax.set_xticklabels([])

    for i, surface in enumerate(row_cats):
        leftmost_ax = axs[i][0]
        if surface == "Overall":
            leftmost_ax.set_ylabel("Overall\nCount", fontsize=10,
                                   rotation=0, labelpad=50)
        else:
            leftmost_ax.set_ylabel(f"{surface}\nCount", fontsize=10,
                                   rotation=0, labelpad=50)
    fig.suptitle(
        "Injury Severity Matrix by Road Surface × Speed Limit",
        fontsize=16,
        y=0.98
    )

    return fig
