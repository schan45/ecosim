import json

class FoodWeb:
    """
    A class to represent and query an ecological food web based on a JSON file.
    """
    
    def __init__(self, filepath):
        """
        Initialize the FoodWeb by loading data from a JSON file.
        
        Parameters:
        filepath (str): Path to the JSON file containing organisms and predation data.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.organisms = data["organisms"]
            self.web = data["predation"]

    def get_prey(self, predator):
        """
        Get the list of prey species for a given predator.
        
        Parameters:
        predator (str): Name of the predator species.
        
        Returns:
        list: List of prey species names.
        """
        return self.web.get(predator, [])

    def get_predators(self, species):
        """
        Get the list of predators for a given species.
        
        Parameters:
        species (str): Name of the species to check for predators.
        
        Returns:
        list: List of predator species names.
        """
        return [pred for pred, prey_list in self.web.items() if species in prey_list]

    def is_prey(self, predator, prey):
        """
        Check if a species is prey to a given predator.
        
        Parameters:
        predator (str): Name of the predator.
        prey (str): Name of the prey.
        
        Returns:
        bool: True if prey is in the predator's prey list, False otherwise.
        """
        return prey in self.web.get(predator, [])

    def is_predator(self, prey, predator):
        """
        Check if a species is a predator to a given prey.
        
        Parameters:
        prey (str): Name of the prey.
        predator (str): Name of the predator.
        
        Returns:
        bool: True if predator preys on the given species, False otherwise.
        """
        return self.is_prey(predator, prey)

    def all_species(self):
        """
        Get a list of all species in the food web.
        
        Returns:
        list: List of species names.
        """
        return list(self.organisms.keys())

    def get_type(self, species):
        """
        Get the type (e.g. producer, consumer) of a species.
        
        Parameters:
        species (str): Name of the species.
        
        Returns:
        str: Type of the species, or 'Unknown' if not specified.
        """
        return self.organisms.get(species, {}).get("type", "Unknown")

    def get_trophic_level(self, species):
        """
        Get the trophic level of a species.
        
        Parameters:
        species (str): Name of the species.
        
        Returns:
        str: Trophic level of the species, or 'unknown' if not specified.
        """
        return self.organisms.get(species, {}).get("trophic_level", "unknown")

    def get_color(self, species):
        """
        Get the display color associated with a species.
        
        Parameters:
        species (str): Name of the species.
        
        Returns:
        str: Hex color code, or '#000000' (black) if not specified.
        """
        return self.organisms.get(species, {}).get("color", "#000000")

    def get_decomposition_rate(self, species):
        """
        Get the decomposition rate of a species.
        
        Parameters:
        species (str): Name of the species.
        
        Returns:
        int: Decomposition rate, or 20 if not specified.
        """
        return self.organisms.get(species, {}).get("decomposition_rate", 20)
