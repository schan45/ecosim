import json

class FoodWeb:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.organisms = data["organisms"]
            self.web = data["predation"]

    def get_prey(self, predator):
        return self.web.get(predator, [])

    def get_predators(self, species):
        return [pred for pred, prey_list in self.web.items() if species in prey_list]

    def is_prey(self, predator, prey):
        return prey in self.web.get(predator, [])

    def is_predator(self, prey, predator):
        return self.is_prey(predator, prey)

    def all_species(self):
        return list(self.organisms.keys())

    def get_type(self, species):
        return self.organisms.get(species, {}).get("type", "Unknown")

    def get_trophic_level(self, species):
        return self.organisms.get(species, {}).get("trophic_level", "unknown")

    def get_color(self, species):
        return self.organisms.get(species, {}).get("color", "#000000")  # alap: fekete
    
    def get_decomposition_rate(self, species):
        return self.organisms.get(species, {}).get("decomposition_rate", 20)
