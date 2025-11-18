# PyQT6 Class for Bar Chart Visualization App
from PyQt6.QtWidgets import QMainWindow
from src.utils import load_bike_crash_data

class BarChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram Visualization")
        self.df = load_bike_crash_data()

        # Additional initialization code here