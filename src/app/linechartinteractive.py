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


class App(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Bike Accidents Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        self.df = df
        self.month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December']

        # Prepare data
        self.prepare_data()

        # Matplotlib Figure
        self.fig, self.axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.setCentralWidget(self.canvas)

        # Plot initial charts
        self.plot_charts()

        # Connect hover event
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def prepare_data(self):
        # Monthly by year
        self.monthly_counts = self.df.groupby(['CrashYear', 'CrashMonth']).size().reset_index(name='NumCrashes')
        self.monthly_counts['CrashMonth'] = pd.Categorical(self.monthly_counts['CrashMonth'],
                                                           categories=self.month_order,
                                                           ordered=True)
        self.monthly_counts = self.monthly_counts.sort_values('CrashMonth')

        # Hourly by month
        self.hourly_counts = self.df.groupby(['CrashMonth', 'CrashHour']).size().reset_index(name='NumCrashes')
        self.hourly_counts['CrashMonth'] = pd.Categorical(self.hourly_counts['CrashMonth'],
                                                          categories=self.month_order,
                                                          ordered=True)

    def plot_charts(self):
        colors = plt.cm.tab20.colors

        # --- Top chart: Monthly by Year ---
        self.top_lines = []
        years = sorted(self.monthly_counts['CrashYear'].unique())
        for i, year in enumerate(years):
            data = self.monthly_counts[self.monthly_counts['CrashYear'] == year]
            line, = self.axes[0].plot(data['CrashMonth'], data['NumCrashes'], marker='o',
                                      label=str(year), color=colors[i % 20], alpha=1.0)
            self.top_lines.append(line)

        self.axes[0].set_title('Monthly Bike Accidents by Year')
        self.axes[0].set_ylabel('Number of Accidents')
        self.axes[0].legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
        self.axes[0].grid(True)
        self.axes[0].set_xlim(self.month_order[0], self.month_order[-1])

        # --- Bottom chart: Hourly by Month ---
        self.bottom_lines = []
        for i, month in enumerate(self.month_order):
            data = self.hourly_counts[self.hourly_counts['CrashMonth'] == month]
            if not data.empty:
                line, = self.axes[1].plot(data['CrashHour'], data['NumCrashes'], marker='o',
                                          label=month, color=colors[i % 20], alpha=1.0)
                self.bottom_lines.append(line)

        self.axes[1].set_title('Hourly Bike Accidents by Month')
        self.axes[1].set_xlabel('Hour of Day')
        self.axes[1].set_ylabel('Number of Accidents')
        self.axes[1].legend(title='Month', bbox_to_anchor=(1.05, 1), loc='upper left')
        self.axes[1].grid(True)
        self.axes[1].set_xticks(range(0, 24))

        self.canvas.draw()

    def on_hover(self, event):
        # Check if mouse is over axes
        if event.inaxes is None:
            # Reset all lines
            for line in self.top_lines + self.bottom_lines:
                line.set_alpha(1.0)
            self.canvas.draw_idle()
            return

        hovered = False

        # --- Highlight top chart lines (years) ---
        if event.inaxes == self.axes[0]:
            for line in self.top_lines:
                contains, _ = line.contains(event)
                line.set_alpha(1.0 if contains else 0.2)
                if contains:
                    hovered = True

        # --- Highlight bottom chart lines (months) ---
        if event.inaxes == self.axes[1]:
            for line in self.bottom_lines:
                contains, _ = line.contains(event)
                line.set_alpha(1.0 if contains else 0.2)
                if contains:
                    hovered = True

        if not hovered:
            for line in self.top_lines + self.bottom_lines:
                line.set_alpha(1.0)

        self.canvas.draw_idle()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    df = load_bike_crash_data()

    window = App(df)
    window.show()
    sys.exit(app.exec())