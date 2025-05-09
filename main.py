# main.py
from simulation.engine import SimulationEngine
from core.terrain import Terrain  # vagy: from logic.terrain import Terrain
import os

def main():
    grid_size = 20
    steps = 70

    # Inicializálás
    terrain = Terrain(grid_size)
    engine = SimulationEngine(grid_size=grid_size, steps=steps, foodweb_path="configs/foodweb_config.json")
    engine.terrain = terrain
    
    # Setup és futtatás
    engine.setup()
    engine.run()

if __name__ == "__main__":
    # Töröljük az előző frame-képeket
    if os.path.exists("frames"):
        for f in os.listdir("frames"):
            os.remove(os.path.join("frames", f))
    main()
