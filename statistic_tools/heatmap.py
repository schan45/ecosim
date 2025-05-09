# statistic_tools/heatmap.py

import os
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image, display

def export_heatmaps(heatmaps, output_dir="statistics_plots"):
    """
    During the simulation, the system keeps track of how often each species (e.g., rabbit, fox) appears at different positions on the map. Based on this data, it generates heatmaps—visual representations where color intensity reflects how frequently individuals of a species were present at certain locations.
    The program creates one heatmap per species, then saves each heatmap as a separate PNG image file in a predefined folder (e.g., statistics_plots). This allows the user to later inspect the spatial behavior of each species—seeing, for instance, where rabbits were most active or where foxes tended to cluster.
    """
    for species, heatmap_data in heatmaps.items():
        plt.figure(figsize=(8, 6))
        flipped = np.flipud(heatmap_data)
        plt.imshow(flipped, cmap="YlOrRd", interpolation='bilinear')
        plt.title(f"Heatmap: {species}")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.colorbar()
        plt.tight_layout()
        filepath = os.path.join(output_dir, f"heatmap_{species}.png")
        plt.savefig(filepath)
        plt.close()

def display_heatmap(species: str, path: str = "statistics_plots") -> None:
    """
    This feature allows the user to display a previously saved heatmap image for a specific species (such as fox or rabbit). The system locates the corresponding .png file in the folder where statistical results are stored (e.g., statistics_plots/heatmap_Fox.png) and renders the image on screen. This visualization helps the user understand where individuals of that species most frequently moved or were located during the simulation.
    """
    file_path = os.path.join(path, f"heatmap_{species}.png")
    if os.path.exists(file_path):
        display(Image(filename=file_path))
    else:
        print(f"⚠️ No heatmap image found for species '{species}' at {file_path}")
