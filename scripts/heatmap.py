import sys
from PyQt6 import QtWidgets

from src.app import HeatmapApp

from src.utils import load_bike_crash_data, prepare_crash_geodata
from src.visualization.heatmap import plot_crash_points, plot_crash_hexbin

if __name__ == "__main__":
    # qapp = QtWidgets.QApplication.instance()
    # if not qapp:
    #     qapp = QtWidgets.QApplication(sys.argv)

    # app = HeatmapApp()
    # app.show()
    # app.activateWindow()
    # app.raise_()
    # qapp.exec()

    df = load_bike_crash_data()          
    gdf_web = prepare_crash_geodata(df)  

    # plot_crash_points(gdf_web, basemap_style="street")
    # or show hexbin heatmap
    plot_crash_hexbin(gdf_web, basemap_style="street", gridsize=40) # gray

    import matplotlib.pyplot as plt
    plt.show()
