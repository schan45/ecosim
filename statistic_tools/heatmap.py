import os
import matplotlib.pyplot as plt
import numpy as np


def export_heatmaps(heatmaps, output_dir="statistics_plots"):
    """
    Menti a fajonkénti hőtérképeket PNG formátumban az adott mappába.
    
    """
    for species, heatmap_data in heatmaps.items():
        plt.figure(figsize=(8, 6))
        flipped = np.flipud(heatmap_data)
        plt.imshow(flipped, cmap="YlOrRd", interpolation='bilinear')
        plt.title(f"Hőtérkép: {species}")
        plt.xlabel("X koordináta")
        plt.ylabel("Y koordináta")
        plt.colorbar()
        plt.tight_layout()
        filepath = os.path.join(output_dir, f"heatmap_{species}.png")
        plt.savefig(filepath)
        plt.close()

