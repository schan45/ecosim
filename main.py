# main.py
from simulation.engine import SimulationEngine
from core.terrain import Terrain
import json
import os

def main():
    grid_size = 20
    steps = 32

    # Konfiguráció betöltése (ha létezik)
    terrain_config_path = "configs/terrain_config.json"
    terrain = Terrain(grid_size)
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

if __name__ == "__main__":
    if os.path.exists("frames"):
        for f in os.listdir("frames"):
            os.remove(os.path.join("frames", f))
    main()
