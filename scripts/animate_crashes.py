#!/usr/bin/env python3
"""
Script to create an animated map of crash density over time.
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.visualization.heatmap import animate_crash_density_over_time
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Creating animated crash density map...")
    
    # Create animation (will display interactively)
    fig, anim = animate_crash_density_over_time(
        basemap_style="gray",
        gridsize=40,
        interval=1000,  # 1 second per frame
        figsize=(12, 10)
    )
    
    # Optionally save to file (uncomment to save)
    # anim.save("crash_density_animation.gif", writer="pillow", fps=1)
    
    print("Animation created! Close the window to exit.")
    plt.show()  # This will display the animation and keep it running

