# PyQT6 Class for Bar Chart Visualization App
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QSlider
from src.utils import load_bike_crash_data, filter_data, prepare_crash_geodata
from src.visualization.heatmap import plot_crash_hexbin
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
import pandas as pd
import matplotlib.ticker as mtick
from superqt import QRangeSlider
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np

class SmallMultiplesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Small Multiples Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        self.df = load_bike_crash_data()
        self.cetegories = ['LightCond', 'SpeedLimit', 'BikeAlcFlg', "BikeSex", "RuralUrban"]
        self.injury_order = ["O: No Injury", "C: Possible Injury", "B: Suspected Minor Injury",
                             "A: Suspected Serious Injury", "K: Killed", "Unknown Injury"]

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.cetegories)
        self.dropdown.currentTextChanged.connect(self.update_plot)
        self.layout.addWidget(self.dropdown)

        # Graph
        self.fig, self.axs = plt.subplots(1, 1, figsize=(12, 6))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.layout.addWidget(self.canvas)

        # Initial plot
        self.update_plot(self.cetegories[0])

    def update_plot(self, category):
        self.fig.clf()

        #Category filtering
        categories = self.df[category].dropna().unique()
        #I gave up on filtering lmao, we're only gonna use this once anyways I think i hope kekw
        categories = [c for c in categories if c != "Unknown"]
        categories = [c for c in categories if c != "Other"]
        categories = [c for c in categories if c != "Missing"]
        categories = [c for c in categories if c != "."]
        categories = [c for c in categories if c != "Dark - Unknown Lighting"]
        categories = sorted(categories)

        n_rows = len(categories)
        self.axs = self.fig.subplots(n_rows, 1, sharex=True)
        if n_rows == 1:
            self.axs = [self.axs]

        # Red Color
        cmap = self.adjusted_colormap(cm.YlOrRd, 0.3)
        norm = mcolors.Normalize(vmin=0, vmax=len(self.injury_order) - 1)
        colors = [cmap(norm(i)) for i in range(len(self.injury_order))]

        # Categorical colors
        # colors = plt.cm.Dark2.colors

        for i, cat_val in enumerate(categories):
            ax = self.axs[i]
            data = self.df[self.df[category] == cat_val]
            counts = data['CrashSevr'].value_counts().reindex(self.injury_order, fill_value=0)

            ax.bar(self.injury_order, counts, color=colors[:len(self.injury_order)])
            ax.set_title(f"{category}: {cat_val}")
            ax.set_ylabel("Count")
            ax.grid(True, axis='y')

        self.axs[-1].set_xlabel("Crash Severity")
        self.fig.tight_layout()
        self.canvas.draw()

    def adjusted_colormap(self, cmap, minval=0, maxval=1.0, n=100):
        new_cmap = mcolors.LinearSegmentedColormap.from_list(
            f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
            cmap(np.linspace(minval, maxval, n))
        )
        return new_cmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmallMultiplesApp()
    window.show()
    sys.exit(app.exec())