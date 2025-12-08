from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from src.utils import load_bike_crash_data, filter_data
from src.visualization.severity_matrix import plot_severity_matrix, VALID_SURFACES, BAD_VALUES
import pandas as pd


class SeverityMatrixWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Road Risk Matrix — Injury Severity by Surface × Speed")
        self.resize(1200, 900)

        self.df = load_bike_crash_data()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0) 

        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(10, 0, 10, 10) 
        filter_label = QLabel("Roadway Feature:")
        self.feature_filter = QComboBox()
        self.feature_filter.addItem("Any")

        features = sorted(self.df["RdFeature"].dropna().unique())
        for f in features:
            if self._has_valid_data(f):
                self.feature_filter.addItem(f)

        self.feature_filter.currentIndexChanged.connect(self.update_plot)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.feature_filter)
        # filter_layout.addStretch()
        
        filter_widget = QWidget()
        filter_widget.setLayout(filter_layout)
        layout.addWidget(filter_widget)

        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.update_plot()

    def update_plot(self):
        df_filtered = self.df.copy()

        feature = self.feature_filter.currentText()
        if feature != "Any":
            df_filtered = filter_data(df_filtered, "RdFeature", feature)

        df_clean = df_filtered.dropna(subset=["RdSurface", "SpeedLimit"])

        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        plot_severity_matrix(df_clean, ax=ax)

        self.canvas.draw()
    
    def _has_valid_data(self, feature):
        df_filtered = self.df.copy()
        
        if feature != "Any":
            df_filtered = filter_data(df_filtered, "RdFeature", feature)
        
        df_clean = df_filtered.dropna(subset=["RdSurface", "SpeedLimit"])
        
        if df_clean.empty:
            return False
        
        df_clean["RdSurface"] = df_clean["RdSurface"].astype(str).str.strip()
        df_clean["SpeedLimit"] = df_clean["SpeedLimit"].astype(str).str.strip()
        
        df_clean = df_clean[~df_clean["RdSurface"].isin(BAD_VALUES)]
        df_clean = df_clean[~df_clean["SpeedLimit"].isin(BAD_VALUES)]
        
        df_clean = df_clean[df_clean["RdSurface"].isin(VALID_SURFACES)]
        
        if df_clean.empty:
            return False
        
        surface_counts = df_clean["RdSurface"].value_counts()
        valid_surfaces_with_enough_data = surface_counts[surface_counts >= 20].index.tolist()
        
        if len(valid_surfaces_with_enough_data) == 0:
            return False
        
        df_final = df_clean[df_clean["RdSurface"].isin(valid_surfaces_with_enough_data)]
        
        return len(df_final["RdSurface"].unique()) > 0 and len(df_final["SpeedLimit"].unique()) > 0
