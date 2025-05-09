
import json
import random
from collections import defaultdict

class Terrain:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.map = defaultdict(lambda: "plain")
        self.shelter_occupants = {}
        self.water_counters = defaultdict(lambda: defaultdict(int))
    
    def load_from_config(self, config_path):
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
        tries = 0
        while tries < 100:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.map[(x, y)] == "plain":
                self.map[(x, y)] = terrain_type
                return
            tries += 1

    def generate_water(self):
        patches = max(1, round(self.grid_size / 7))  # reduced size
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
        for _ in range(self.grid_size - 7):
            self._place_random("tree")

    def generate_hills(self):
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
        for _ in range(max(1, round(self.grid_size / 10))):
            for _ in range(4):
                self._place_random("shelter")

    def get_type(self, x, y):
        return self.map.get((x, y), "plain")

    def is_blocked(self, x, y):
        return self.map.get((x, y)) == "tree"

    def is_shelter(self, x, y):
        return self.map.get((x, y)) == "shelter"

    def is_in_shelter(self, x, y):
        return self.map.get((x, y)) == "shelter"

    def is_hill(self, x, y):
        return self.map.get((x, y)) == "hill"

    def is_water(self, x, y):
        return self.map.get((x, y)) == "water"

    def apply_terrain_effects(self, org, step_counter):
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
        for org in organisms:
            pos = (org.x, org.y)
            # 🎯 Ha nem "primary" de menedéken áll
            if self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) != "primary":
                # 💡 Próbáljunk neki találni új, nem shelter pozíciót
                for _ in range(20):  # max 20 próbálkozás
                    new_x = random.randint(0, self.grid_size - 1)
                    new_y = random.randint(0, self.grid_size - 1)
                    if not self.is_shelter(new_x, new_y) and not self.is_blocked(new_x, new_y):
                        org.x = new_x
                        org.y = new_y
                        break
                continue  # ugorjuk át a további shelter logikát

            # ✅ Ha primary, akkor trackeljük a menedékben töltött idejét
            if self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) == "primary":
                if pos not in self.shelter_occupants:
                    self.shelter_occupants[pos] = {}
                count = self.shelter_occupants[pos].get(id(org), 0) + 1
                self.shelter_occupants[pos][id(org)] = count
                if count > 3:
                    org.alive = False  # túl sok időt töltött bent
            else:
                # ❌ már nem shelterben van, töröljük a számlálót
                for data in self.shelter_occupants.values():
                    data.pop(id(org), None)

    
    def can_enter_shelter(self, org):
        return self.is_shelter(org.x, org.y) and getattr(org, "trophic_level", None) == "primary"

