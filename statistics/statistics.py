import os
import shutil
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


STATISTICS_DIR = "statistics_plots"
FRAMES_DIR = "frames"


def clear_statistics_folder(path: str = STATISTICS_DIR) -> None:
    """
    Deletes and recreates the statistics_plots directory to avoid mixing results.
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def heatmap(animal_type: str, frames_path: str = FRAMES_DIR) -> None:
    """
    Creates a heatmap showing animal density over simulation frames.
    """
    positions = []
    for fname in sorted(os.listdir(frames_path)):
        if fname.endswith(".json"):
            with open(os.path.join(frames_path, fname)) as f:
                data = json.load(f)
                animals = data.get("animals", [])
                for animal in animals:
                    if animal.get("type") == animal_type:
                        pos = animal.get("position")
                        if pos:
                            positions.append(tuple(pos))

    if not positions:
        print(f"No positions found for animal type '{animal_type}'.")
        return

    x, y = zip(*positions)
    heatmap_grid, xedges, yedges = np.histogram2d(x, y, bins=(50, 50))

    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_grid.T, cmap="viridis")
    plt.title(f"Heatmap of {animal_type} positions")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(os.path.join(STATISTICS_DIR, f"heatmap_{animal_type}.png"))
    plt.close()


def population_trend(animal_type: str, frames_path: str = FRAMES_DIR) -> None:
    """
    Plots the number of a specific animal type over time.
    """
    counts = []
    frame_indices = []

    for idx, fname in enumerate(sorted(os.listdir(frames_path))):
        if fname.endswith(".json"):
            with open(os.path.join(frames_path, fname)) as f:
                data = json.load(f)
                animals = data.get("animals", [])
                count = sum(1 for a in animals if a.get("type") == animal_type)
                counts.append(count)
                frame_indices.append(idx)

    if not counts:
        print(f"No animals of type '{animal_type}' found.")
        return

    plt.figure(figsize=(8, 6))
    plt.plot(frame_indices, counts, marker="o")
    plt.title(f"Population trend of {animal_type}")
    plt.xlabel("Simulation step")
    plt.ylabel("Count")
    plt.grid(True)
    plt.savefig(os.path.join(STATISTICS_DIR, f"population_trend_{animal_type}.png"))
    plt.close()
