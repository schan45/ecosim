import json
import random
from collections import defaultdict

class Terrain:
    """
    Represents the terrain grid used in the ecosystem simulation, including terrain types and their effects.

    Attributes:
        grid_size (int): The size of the square simulation grid.
        map (defaultdict): A mapping of (x, y) positions to terrain types.
        shelter_occupants (dict): Tracks the occupancy of shelters by organisms.
        water_counters (defaultdict): Tracks energy boosts from water for individual organisms.
    """

    def __init__(self, grid_size):
        """
        Initializes the terrain grid with default terrain type "plain".

        Args:
            grid_size (int): Size of the simulation grid.
        """
        self.grid_size = grid_size
        self.map = defaultdict(lambda: "plain")
        self.shelter_occupants = {}
        self.water_counters = defaultdict(lambda: defaultdict(int))

    def load_from_config(self, config_path):
        """
        Loads terrain layout from a configuration file. Supports 'random' or 'manual' terrain placement.

        Args:
            config_path (str): Path to the JSON configuration file.
        """
        with open(config_path, 'r') as f:
            data = json.load(f)

        mode = data.get("mode", "random")
        if mode == "random":
            self.generate_water()
            self.generate_trees()
            self.generate_hills()
            self.generate_shelters()
        elif mode == "manual":
            for obj in data.get("terrain_objects", []):
                ttype = obj["type"]
                x0 = obj["x"]
                y0 = obj["y"]
                width = obj.get("width", 1)
                height = obj.get("height", 1)

                for dx in range(width):
                    for dy in range(height):
                        x = x0 + dx
                        y = y0 + dy
                        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                            self.map[(x, y)] = ttype

    def _place_random(self, terrain_type):
        """
        Randomly places a terrain type on an unoccupied plain tile.

        Args:
            terrain_type (str): The type of terrain to place (e.g., 'tree', 'shelter').
        """
        tries = 0
        while tries < 100:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.map[(x, y)] == "plain":
                self.map[(x, y)] = terrain_type
                return
            tries += 1

    def generate_water(self):
        """
        Generates water patches randomly across the terrain.
        """
        patches = max(1, round(self.grid_size / 7))
        for _ in range(patches):
            cx = random.randint(2, self.grid_size - 3)
            cy = random.randint(2, self.grid_size - 3)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                        if self.map[(x, y)] == "plain":
                            self.map[(x, y)] = "water"

    def generate_trees(self):
        """
        Randomly places individual trees throughout the grid.
        """
        for _ in range(self.grid_size - 7):
            self._place_random("tree")

    def generate_hills(self):
        """
        Generates small clusters of 'hill' terrain types.
        """
        patches = round(self.grid_size / 6)
        for _ in range(patches):
            cx = random.randint(2, self.grid_size - 3)
            cy = random.randint(2, self.grid_size - 3)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                        if self.map[(x, y)] == "plain":
                            self.map[(x, y)] = "hill"

    def generate_shelters(self):
        """
        Randomly places multiple 'shelter' locations on the terrain.
        """
        for _ in range(max(1, round(self.grid_size / 10))):
            for _ in range(4):
                self._place_random("shelter")

    def get_type(self, x, y):
        """
        Returns the terrain type at a given coordinate.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            str: Terrain type at the specified location.
        """
        return self.map.get((x, y), "plain")

    def is_blocked(self, x, y):
        """
        Checks if a tile is blocked due to a tree.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if tile contains a tree.
        """
        return self.map.get((x, y)) == "tree"

    def is_shelter(self, x, y):
        """
        Checks if a tile is a shelter.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if tile is a shelter.
        """
        return self.map.get((x, y)) == "shelter"

    def is_in_shelter(self, x, y):
        """
        Alias for is_shelter() for compatibility.

        Returns:
            bool: True if the position is a shelter.
        """
        return self.is_shelter(x, y)

    def is_hill(self, x, y):
        """
        Checks if a tile is a hill.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if tile is a hill.
        """
        return self.map.get((x, y)) == "hill"

    def is_water(self, x, y):
        """
        Checks if a tile is water.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True if tile is water.
        """
        return self.map.get((x, y)) == "water"

    def apply_terrain_effects(self, org, step_counter):
        """
        Applies terrain-based effects to an organism, such as energy gain near water.

        Args:
            org (Organism): The organism affected.
            step_counter (int): Current simulation step counter.
        """
        if step_counter % 10 != 0 or not org.alive or hasattr(org, "is_edible"):
            return
        adjacent = [(org.x + dx, org.y + dy)
                    for dx in [-1, 0, 1]
                    for dy in [-1, 0, 1]
                    if (dx != 0 or dy != 0)
                    and 0 <= org.x + dx < self.grid_size
                    and 0 <= org.y + dy < self.grid_size]
        for pos in adjacent:
            if self.is_water(*pos):
                counter = self.water_counters[pos][id(org)]
                if counter < 2:
                    org.energy = min(org.max_energy, org.energy + 5)
                    self.water_counters[pos][id(org)] += 1
                    break

    def update_shelters(self, organisms):
        """
        Updates organism interactions with shelter tiles. Carnivores are pushed out,
        while herbivores gain temporary protection or die if they stay too long.

        Args:
            organisms (list): List of organisms to update.
        """
        for org in organisms:
            pos = (org.x, org.y)

            if self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) != "primary":
                # Carnivores get ejected from shelters
                for _ in range(20):
                    new_x = random.randint(0, self.grid_size - 1)
                    new_y = random.randint(0, self.grid_size - 1)
                    if not self.is_shelter(new_x, new_y) and not self.is_blocked(new_x, new_y):
                        org.x = new_x
                        org.y = new_y
                        break
                continue  

            if self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) == "primary":
                # Herbivores in shelter
                if pos not in self.shelter_occupants:
                    self.shelter_occupants[pos] = {}
                count = self.shelter_occupants[pos].get(id(org), 0) + 1
                self.shelter_occupants[pos][id(org)] = count
                if count > 3:
                    org.alive = False  
            else:
                # Clear shelter counter if not in shelter
                for data in self.shelter_occupants.values():
                    data.pop(id(org), None)

    def can_enter_shelter(self, org):
        """
        Checks if a given organism is allowed to enter the current shelter tile.

        Args:
            org (Organism): The organism to check.

        Returns:
            bool: True if organism is a primary consumer in a shelter.
        """
        return self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) == "primary"
