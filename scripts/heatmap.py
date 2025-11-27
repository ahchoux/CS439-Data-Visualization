import matplotlib.pyplot as plt
from src.utils import load_bike_crash_data, prepare_crash_geodata
from src.visualization.heatmap import plot_crash_hexbin

if __name__ == "__main__":
    df = load_bike_crash_data()          
    gdf_web = prepare_crash_geodata(df)  
    plot_crash_hexbin(gdf_web, basemap_style="street", gridsize=40) # gray

    plt.show()
