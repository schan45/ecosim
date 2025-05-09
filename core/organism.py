import random
import logic.behavior as behavior

class Organism:
    """
    Base class representing a general organism in the ecosystem simulation.

    Attributes:
        species (str): The name of the species.
        x (int): X-coordinate on the grid.
        y (int): Y-coordinate on the grid.
        energy (int): Current energy level of the organism.
        max_energy (int): Maximum energy the organism can have.
        alive (bool): Indicates whether the organism is alive.
    """
    def __init__(self, species_name, x, y, energy=100, max_energy=120):
        """
        Initializes an Organism instance with a species name, coordinates, and energy levels.

        Args:
            species_name (str): The species name.
            x (int): X-coordinate.
            y (int): Y-coordinate.
            energy (int, optional): Starting energy. Defaults to 100.
            max_energy (int, optional): Maximum energy. Defaults to 120.
        """
        self.species = species_name
        self.x = x
        self.y = y
        self.energy = energy
        self.max_energy = max_energy
        self.alive = True

    def step(self, grid_size):
        """
        Simulates one time step for the organism, reducing its energy.
        If energy reaches zero or below, the organism dies.

        Args:
            grid_size (int): Size of the simulation grid (unused here).
        """
        if not self.alive:
            return
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False    

    def __repr__(self):
        """
        Returns a string representation of the organism for debugging/logging.

        Returns:
            str: Formatted string with species name, position, and energy.
        """
        return f"{self.species}({self.x},{self.y},E={self.energy})"

# ----------------------------------------------------------------------------------

class Producer(Organism):
    """
    Represents plant-like entities in the ecosystem that do not move.

    Attributes:
        is_edible (bool): Whether the producer can be consumed by other organisms.
    """
    def __init__(self, species_name, x, y):
        """
        Initializes a Producer at a given location with default energy.

        Args:
            species_name (str): The species name.
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        super().__init__(species_name, x, y, energy=100)  
        self.is_edible = True

    def step(self, grid_size):
        """
        Defines the behavior of the producer in each time step.
        Producers do not perform actions, so this is a no-op.

        Args:
            grid_size (int): Size of the simulation grid (unused).
        """
        pass

# ----------------------------------------------------------------------------------

class Consumer(Organism):
    """
    Represents mobile, decision-making animal entities in the ecosystem.

    Attributes:
        trophic_level (str): The trophic level (e.g., 'primary', 'secondary').
        speed (int): Maximum number of grid cells the consumer can move per step.
    """
    def __init__(self, species_name, x, y, trophic_level='primary', speed=1):
        """
        Initializes a Consumer with position, energy, and behavior attributes.

        Args:
            species_name (str): The species name.
            x (int): X-coordinate.
            y (int): Y-coordinate.
            trophic_level (str, optional): Trophic level. Defaults to 'primary'.
            speed (int, optional): Movement speed. Defaults to 1.
        """
        super().__init__(species_name, x, y, energy=100, max_energy=120)
        self.trophic_level = trophic_level
        self.speed = speed

    def move(self, grid_size):
        """
        Moves the consumer randomly within the bounds of the grid.

        Args:
            grid_size (int): Size of the simulation grid.
        """
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        self.x = max(0, min(grid_size - 1, self.x + dx))
        self.y = max(0, min(grid_size - 1, self.y + dy))

    def step(self, grid_size, others, foodweb, behavior, terrain=None):
        """
        Executes one simulation step where the consumer may perform:
        - fleeing from threats
        - chasing prey
        - attempting to eat
        - moving randomly

        Args:
            grid_size (int): Size of the grid.
            others (list): Other organisms in the environment.
            foodweb (FoodWeb): Object representing food chain relationships.
            behavior (module): Module containing decision-making logic.
            terrain (optional): Grid terrain, possibly affecting movement.
        """
        if not self.alive:
            return

        behavior.flee(self, others, foodweb)
        behavior.chase(self, others, foodweb)
        behavior.eat_if_possible(self, others, foodweb)
        behavior.random_move(self, grid_size, terrain)

        self.energy -= 1
        if self.energy <= 0:
            self.alive = False
