# PyQT6 Class for Heatmap Visualization App
from PyQt6.QtWidgets import QMainWindow
from src.utils import load_bike_crash_data

class HeatmapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heatmap Visualization")
        self.df = load_bike_crash_data()

        # Additional initialization code here