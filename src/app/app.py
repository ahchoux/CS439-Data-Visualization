# PyQT6 Class for Bar Chart Visualization App
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QSlider
from src.utils import load_bike_crash_data, filter_data, prepare_crash_geodata
from src.visualization.heatmap import plot_crash_hexbin
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
import pandas as pd
import matplotlib.ticker as mtick


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = load_bike_crash_data()
        self.resize(1400, 850)

        # Label
        self.injury_order = ["O: No Injury", "C: Possible Injury", "B: Suspected Minor Injury",
                             "A: Suspected Serious Injury", "K: Killed", "Unknown Injury"]
        self.pretty_injury_labels = {
            "O: No Injury": "No Injury",
            "C: Possible Injury": "Possible Injury",
            "B: Suspected Minor Injury": "Suspected Minor Injury",
            "A: Suspected Serious Injury": "Suspected Serious Injury",
            "K: Killed": "Killed",
            "Unknown Injury": "Unknown Injury"
        }
        self.months = ["Any", "January", "February", "March", "April", "May", "June", "July",
                       "August", "September", "October", "November", "December"]

        self.setWindowTitle("Bike Accidents by Severity")

        # --- Layout ---
        layout = QVBoxLayout()
        filter_row = QHBoxLayout()
        filter_row2 = QHBoxLayout()

        # --- Filters ---
        # Alcohol filter
        filter_row.addWidget(QLabel("Alcohol involvement:"))
        self.alcohol_filter = QComboBox()
        self.alcohol_filter.addItems(["Any", "Yes", "No"])
        self.alcohol_filter.currentIndexChanged.connect(self.update_plot)
        filter_row.addWidget(self.alcohol_filter)

        # HitRun filter
        filter_row.addWidget(QLabel("Hit and Run:"))
        self.hitrun_filter = QComboBox()
        self.hitrun_filter.addItems(["Any", "Yes", "No"])
        self.hitrun_filter.currentIndexChanged.connect(self.update_plot)
        filter_row.addWidget(self.hitrun_filter)

        # LightCond
        filter_row.addWidget(QLabel("Light Conditions: "))
        self.lightcond_filter = QComboBox()
        self.lightcond_filter.addItems(
            ["Any", "Daylight", "Dark - Lighted Roadway", "Dark - Roadway Not Lighted", "Dusk",
             "Dawn"])
        self.lightcond_filter.currentIndexChanged.connect(self.update_plot)
        filter_row.addWidget(self.lightcond_filter)

        # BikePos
        filter_row2.addWidget(QLabel("Bike Position: "))
        self.bikepos_filter = QComboBox()
        self.bikepos_filter.addItems(
            ["Any", "Travel Lane", "Sidewalk / Crosswalk / Driveway Crossing", "Bike Lane / Paved Shoulder",
             "Non-Roadway", "Unknown"])
        self.bikepos_filter.currentIndexChanged.connect(self.update_plot)
        filter_row2.addWidget(self.bikepos_filter)

        # TraffCntrl
        filter_row2.addWidget(QLabel("Traffic Control: "))
        self.traffcntrl_filter = QComboBox()
        self.traffcntrl_filter.addItems(
            ["Any", "No Control Present", "Stop Sign", "Stop And Go Signal",
             "Double Yellow Line, No Passing Zone", "Missing"])
        self.traffcntrl_filter.currentIndexChanged.connect(self.update_plot)
        filter_row2.addWidget(self.traffcntrl_filter)

        # SpeedLimit
        filter_row2.addWidget(QLabel("Speed Limit: "))
        self.speedlimit_filter = QComboBox()
        self.speedlimit_filter.addItems(
            ["Any", "5 - 15 MPH", "20 - 25  MPH", "30 - 35  MPH",
             "40 - 45  MPH", "50 - 55  MPH"])
        self.speedlimit_filter.currentIndexChanged.connect(self.update_plot)
        filter_row2.addWidget(self.speedlimit_filter)

        # --- Time Slider ---
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Time of Day:"))
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setMinimum(-1)  # -1 = Any
        self.time_slider.setMaximum(23)  # Hours 0–23
        self.time_slider.setValue(-1)  # Default: Any
        self.time_slider.setTickInterval(1)
        self.time_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.time_slider.valueChanged.connect(self.update_plot)
        time_layout.addWidget(self.time_slider)
        self.time_label = QLabel("Any")
        time_layout.addWidget(self.time_label)

        # --- Month Slider ---
        month_layout = QHBoxLayout()
        month_layout.addWidget(QLabel("Month:"))
        self.month_slider = QSlider(Qt.Orientation.Horizontal)
        self.month_slider.setMinimum(0)  # -1 = Any
        self.month_slider.setMaximum(12)  # Months: 1-12
        self.month_slider.setValue(0)  # Default: Any
        self.month_slider.setTickInterval(1)
        self.month_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.month_slider.valueChanged.connect(self.update_plot)
        month_layout.addWidget(self.month_slider)
        self.month_label = QLabel("Any")
        self.month_label.setFixedWidth(60)
        month_layout.addWidget(self.month_label)

        # --- Matplotlib figure Histogram ---
        self.figure_hist = Figure(figsize=(12, 8))
        self.canvas_hist = FigureCanvasQTAgg(self.figure_hist)

        # --- Matplotlib figure Heatmap ---
        self.figure_heatmap = Figure(figsize=(12, 8))
        self.canvas_heatmap = FigureCanvasQTAgg(self.figure_heatmap)

        # Horizontal container for both plots and a key-takeaways section
        plots_row = QHBoxLayout()
        plots_col = QVBoxLayout()
        self.info_box = QLabel("")
        self.info_box.setStyleSheet("""
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        """)
        plots_col.addWidget(self.canvas_heatmap, stretch=4)
        plots_col.addWidget(self.info_box, stretch=1)
        
        plots_row.addWidget(self.canvas_hist, stretch=1)
        plots_row.addLayout(plots_col, stretch=2)

        layout.addLayout(plots_row, stretch=1)
        layout.addLayout(filter_row, stretch=0)
        layout.addLayout(filter_row2, stretch=0)
        layout.addLayout(time_layout, stretch=0)
        layout.addLayout(month_layout, stretch=0)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.update_plot()

    def update_plot(self):
        df_filtered = self.df.copy()

        # Apply alcohol filter
        alcohol_choice = self.alcohol_filter.currentText()
        df_filtered = filter_data(df_filtered, "CrashAlcoh", alcohol_choice)

        # Apply hit and run filter
        hitrun_choice = self.hitrun_filter.currentText()
        df_filtered = filter_data(df_filtered, "HitRun", hitrun_choice)

        # Apply LightCond filter
        lightcond_choice = self.lightcond_filter.currentText()
        df_filtered = filter_data(df_filtered, "LightCond", lightcond_choice)

        # Apply BikePos filter
        bikepos_choice = self.bikepos_filter.currentText()
        df_filtered = filter_data(df_filtered, "BikePos", bikepos_choice)

        # Apply TraffCntrl filter
        traffcntrl_choice = self.traffcntrl_filter.currentText()
        df_filtered = filter_data(df_filtered, "TraffCntrl", traffcntrl_choice)

        # Apply SpeedLimit filter
        speedlimit_choice = self.speedlimit_filter.currentText()
        df_filtered = filter_data(df_filtered, "SpeedLimit", speedlimit_choice)

        # Apply hour filter
        hour_choice = self.time_slider.value()
        if hour_choice == -1:
            self.time_label.setText("Any")
        else:
            self.time_label.setText(str(hour_choice))
            df_filtered = filter_data(df_filtered, "CrashHour", hour_choice)

        # Apply month filter
        month_choice = self.months[self.month_slider.value()]
        self.month_label.setText(month_choice)
        df_filtered = filter_data(df_filtered, "CrashMonth", month_choice)

        # -0---------------- Plot heatmap ---------------------
        
        # Clear previous plot
        self.figure_heatmap.clear()
        ax = self.figure_heatmap.add_subplot(1, 1, 1)
        
        gdf_web = prepare_crash_geodata(df_filtered)
        plot_crash_hexbin(gdf_web, basemap_style="street", gridsize=40, ax=ax)
        self.canvas_heatmap.draw()
        
        # ----------------- Plot histogram ---------------------

        # Clear previous plot
        self.figure_hist.clear()
        ax = self.figure_hist.add_subplot(1, 1, 1)


        num_filtered = len(df_filtered)
        counts = df_filtered["BikeInjury"].value_counts()
        num_filtered = len(df_filtered)
        counts = df_filtered["BikeInjury"].value_counts()

        if num_filtered == 0:
            ordered_counts = [0 for _ in self.injury_order]
        else:
            ordered_counts = [100 * counts.get(cat, 0) / num_filtered for cat in self.injury_order]
        ax.bar(self.injury_order, ordered_counts)
        ax.set_xticks(range(len(self.injury_order)))
        ax.set_xticklabels([self.pretty_injury_labels[label] for label in self.injury_order], rotation=25, ha="right", fontsize=8)

        ax.set_title(f"Bike Injury By Severity")
        ax.set_xlabel("Injury Severity")
        ax.set_ylabel("Percentage of Accidents")
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f%%'))

        # shift hist up a to avoid cutting off category labels
        self.figure_hist.subplots_adjust(left=0.2, bottom=0.2)
        
        self.canvas_hist.draw()
        
        # Update Info Box
        most_common_biker_age_group = self._get_most_common_category(df_filtered, 'BikeAgeGrp')
        most_common_driver_age_group = self._get_most_common_category(df_filtered, 'DrvrAgeGrp')
        most_common_biker_direction = self._get_most_common_category(df_filtered, 'BikeDir')
        most_common_crash_loc = self._get_most_common_category(df_filtered, 'CrashLoc')
        most_common_scenario = self._get_most_common_category(df_filtered, 'CrashGrp')
        most_common_vehicle_type = self._get_most_common_category(df_filtered, 'DrvrVehTyp')
        driver_alcohol_rate = df_filtered['DrvrAlcFlg'].value_counts(normalize=True).get('Yes', 0) * 100 if not df_filtered.empty else 0
        hit_and_run_rate = df_filtered['HitRun'].value_counts(normalize=True).get('Yes', 0) * 100 if not df_filtered.empty else 0
        info_text = f"""
<b>Additional Filtered Info: ({len(df_filtered):,} accidents)</b><br>
<table style="border-spacing: 50px 5px; text-align: left;">
<tr>
<td> <u>Most Common Biker Age Group</u>: {most_common_biker_age_group}</td>
<td> <u>Most Common Crash Location</u>: {most_common_crash_loc}</td>
</tr>
<tr>
<td> <u>Most Common Driver Age Group</u>: {most_common_driver_age_group}</td>
<td> <u>Most Common Crash Scenario</u>: {most_common_scenario}</td>
</tr>
<tr>
<td> <u>Most Common Biker Direction</u>: {most_common_biker_direction}</td>
<td> <u>Most Common Vehicle Type Involved</u>: {most_common_vehicle_type}</td>
</tr>
<tr>
<td> <u>Driver Alcohol Involvement Rate</u>: {driver_alcohol_rate:.1f}%</td>
<td> <u>Hit and Run Rate</u>: {hit_and_run_rate:.1f}%</td>
<td></td>
</tr>
</table>
        """
        self.info_box.setText(info_text)
    
    def _get_avg(self, df: pd.DataFrame, column: str) -> str:
        if df.empty:
            return "N/A"
        avg_value = df[column].str.replace(r'\D', '', regex=True).astype(int).mean()
        if pd.isna(avg_value):
            return "N/A"
        return f"{avg_value:.1f}"
    
    def _get_most_common_category(self, df: pd.DataFrame, column: str) -> str:
        if df.empty:
            return "N/A"
        mode_series = df[column].mode()
        if mode_series.empty:
            return "N/A"
        
        cat = mode_series.iloc[0]
        percentage = (df[column] == cat).sum() * 100 / len(df)
        return f"{cat} ({percentage:.1f}%)"

#TESTING
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())