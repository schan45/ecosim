
from core.organism import Consumer, Producer
from core.foodweb import FoodWeb
import logic.behavior as behavior
from visualizer.plot import plot_organisms
import random
from logic.reproduction import reproduce
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statistic_tools.heatmap import export_heatmaps
from statistic_tools.population import export_population_chart


class SimulationEngine:
    def __init__(self, grid_size=20, steps=30, foodweb_path="configs/foodweb_config.json"):
        self.grid_size = grid_size
        self.steps = steps
        self.foodweb = FoodWeb(foodweb_path)
        self.organisms = []
        self.heatmaps = defaultdict(lambda: np.zeros((self.grid_size, self.grid_size), dtype=int))
        self.population_history = defaultdict(list)
        self.terrain = None  # később beállítandó kívülről, pl. terrain = Terrain(...)

    def setup(self):
        level_counts = {
            "primary": 5,
            "secondary": 2,
            "tertiary": 1,
            "omnivore": 3,
            "unknown": 1
        }

        for species in self.foodweb.all_species():
            org_type = self.foodweb.get_type(species)

            if org_type == "Producer":
                for _ in range(4):
                    while True:
                        x = random.randint(0, self.grid_size - 1)
                        y = random.randint(0, self.grid_size - 1)
                        occupied = any(o.x == x and o.y == y for o in self.organisms)
                        blocked = self.terrain and (self.terrain.is_water(x, y) or self.terrain.is_blocked(x, y))
                        if not occupied and not blocked:
                            break
                    self.organisms.append(Producer(species, x, y))

            elif org_type == "Consumer":
                trophic_level = self.foodweb.get_trophic_level(species)
                count = self.foodweb.organisms[species].get("initial_count", level_counts.get(trophic_level, 1))
                for _ in range(count):
                    while True:
                        x = random.randint(0, self.grid_size - 1)
                        y = random.randint(0, self.grid_size - 1)
                        occupied = any(o.x == x and o.y == y for o in self.organisms)
                        blocked = self.terrain and (self.terrain.is_water(x, y) or self.terrain.is_blocked(x, y))
                        if not occupied and not blocked:
                            break
                    self.organisms.append(Consumer(species, x, y, trophic_level=trophic_level))


        reproduce._foodweb = self.foodweb
        reproduce._terrain = self.terrain
        # --- Decomposer interval kiszámítása ---
        decomposer_species = [
            s for s in self.foodweb.all_species()
            if self.foodweb.get_type(s) == "Decomposer"
        ]
        self.decomposition_interval = min(
            [self.foodweb.get_decomposition_rate(s) for s in decomposer_species],
            default=20
        )


    def run(self):
        for step in range(self.steps):
            print(f"\n--- Step {step} ---")
            living = [org for org in self.organisms if org.alive]

            for org in living:
                if isinstance(org, Consumer):
                    org.step(self.grid_size, self.organisms, self.foodweb, behavior, self.terrain)
                elif isinstance(org, Producer):
                    org.step(self.grid_size)

                if self.terrain:
                    self.terrain.apply_terrain_effects(org, step)
                
                if 0 <= org.x < self.grid_size and 0 <= org.y < self.grid_size:
                    self.heatmaps[org.species][org.y, org.x] += 1  

            if self.terrain:
                self.terrain.update_shelters(self.organisms)

            for org in self.organisms:
                status = "X" if not org.alive else ""
                print(f"{org} {status}")

            newbies = reproduce(self.organisms, self.grid_size, step)
            self.organisms.extend(newbies)

            species_counts = defaultdict(int)
            for org in self.organisms:
                if org.alive:
                    species_counts[org.species] += 1

            for species in self.foodweb.all_species():
                self.population_history[species].append(species_counts.get(species, 0))

                        # --- Globális dekompozíció ---
            if step > 0 and step % self.decomposition_interval == 0:
                for corpse in self.organisms:
                    if not corpse.alive:
                        print(f"💀 Decomposed: {corpse}")
                        self.organisms.remove(corpse)
                        break


            plot_organisms(step, self.organisms, self.grid_size, foodweb=self.foodweb, terrain=self.terrain)
            
            export_population_chart(self.population_history)

        for species, heatmap_data in self.heatmaps.items():
            plt.figure(figsize=(8, 6))
            plt.imshow(heatmap_data, cmap="YlOrRd", interpolation='bilinear')
            plt.title(f"Hőtérkép: {species}")
            plt.xlabel("X koordináta")
            plt.ylabel("Y koordináta")
            plt.colorbar()
            plt.tight_layout()
            plt.close()

        export_heatmaps(self.heatmaps)