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

if __name__ == '__main__':
    df = load_bike_crash_data()

    #---Month Data---
    monthly_counts = df.groupby(['CrashYear', 'CrashMonth']).size().reset_index(name='NumCrashes')

    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_counts['CrashMonth'] = pd.Categorical(monthly_counts['CrashMonth'],
                                                  categories=month_order,
                                                  ordered=True)
    monthly_counts = monthly_counts.sort_values('CrashMonth')

    #---Hour Data---
    hourly_counts = df.groupby(['CrashMonth', 'CrashHour']).size().reset_index(name='NumCrashes')
    hourly_counts['CrashMonth'] = pd.Categorical(hourly_counts['CrashMonth'],
                                                 categories=month_order,
                                                 ordered=True)

    colors = plt.cm.tab20.colors

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=False)
    #Plot month line chart
    ax1 = axes[0]
    years = sorted(monthly_counts['CrashYear'].unique())
    for i, year in enumerate(years):
        data = monthly_counts[monthly_counts['CrashYear'] == year]
        ax1.plot(data['CrashMonth'], data['NumCrashes'], marker='o',
                 label=str(year), color=colors[i % 20])

    ax1.set_title('Monthly Bike Accidents by Year')
    ax1.set_ylabel('Number of Accidents')
    ax1.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True)
    ax1.set_xlim(month_order[0], month_order[-1])

    #Plot Hour Line chart
    ax2 = axes[1]
    for i, month in enumerate(month_order):
        data = hourly_counts[hourly_counts['CrashMonth'] == month]
        if not data.empty:
            ax2.plot(data['CrashHour'], data['NumCrashes'], marker='o',
                     label=month, color=colors[i % 20])

    ax2.set_title('Hourly Bike Accidents by Month')
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Number of Accidents')
    ax2.legend(title='Month', bbox_to_anchor=(1.05, 1), loc='upper left')  # legend outside
    ax2.grid(True)
    ax2.set_xticks(range(0, 24))
    ax2.set_xlim(0, 23)

    plt.tight_layout()
    plt.show()

