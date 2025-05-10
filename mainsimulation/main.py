"""
Main entry point for the ecosystem simulation.

Handles setup for output directories, terrain configuration, and executes the simulation.
"""

from simulation.engine import SimulationEngine
from core.terrain import Terrain
import json
import os
import shutil

# --- Setup for saving statistical outputs ---
stats_dir = "statistics_plots"
if os.path.exists(stats_dir):
    shutil.rmtree(stats_dir)
os.makedirs(stats_dir)

# --- Clean up previous simulation frames ---
if os.path.exists("frames"):
    for f in os.listdir("frames"):
        os.remove(os.path.join("frames", f))

def simulation(grid_size, steps):
    """
    Initialize terrain, configure simulation engine and run the simulation.

    Parameters:
    grid_size (int): Size of the simulation grid (NxN).
    steps (int): Number of simulation steps to execute.
    """
    terrain_config_path = "configs/terrain_config.json"
    terrain = Terrain(grid_size)
    
    # Load terrain config if available, otherwise generate random terrain
    if os.path.exists(terrain_config_path):
        terrain.load_from_config(terrain_config_path)
    else:
        terrain.generate_water()
        terrain.generate_trees()
        terrain.generate_hills()
        terrain.generate_shelters()

    engine = SimulationEngine(grid_size=grid_size, steps=steps, foodweb_path="configs/foodweb_config.json")
    engine.terrain = terrain
    engine.setup()
    engine.run()
