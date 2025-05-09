import random
import logic.behavior as behavior

class Organism:
    def __init__(self, species_name, x, y, energy=100, max_energy=120):
        self.species = species_name
        self.x = x
        self.y = y
        self.energy = energy
        self.max_energy = max_energy
        self.alive = True

    def step(self, grid_size):
        if not self.alive:
            return
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False    

    def __repr__(self):
        return f"{self.species}({self.x},{self.y},E={self.energy})"

# ----------------------------------------------------------------------------------

class Producer(Organism):
    """The program defines various entities, or individuals, which include not only animals but also plants. These plant entities — unlike animals — are not capable of movement, meaning they remain in the same position throughout the simulation."""
    def __init__(self, species_name, x, y):
        super().__init__(species_name, x, y, energy=100)  
        self.is_edible = True

    def step(self, grid_size):
        
        pass

# ----------------------------------------------------------------------------------

class Consumer(Organism):
    """Animal entities in the simulation exhibit active behaviors, such as movement, hunting, and fleeing. These motion-based actions are an essential part of the system's dynamics: animals search for food, respond to threats, and interact with other organisms. This distinguishes them from plants, which are static and do not engage in such activities. The program therefore treats animals as mobile, decision-making entities."""
    def __init__(self, species_name, x, y, trophic_level='primary', speed=1):
        super().__init__(species_name, x, y, energy=100, max_energy=120)
        self.trophic_level = trophic_level
        self.speed = speed


    def move(self, grid_size):
        """In the program, animal movement generally follows a random pattern. This means that individuals do not move along a predefined path, but instead choose their direction randomly at each step. This type of motion simulates natural behavior, where animals often roam aimlessly until they detect food, a predator, or some other external stimulus that influences their movement."""
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        self.x = max(0, min(grid_size - 1, self.x + dx))
        self.y = max(0, min(grid_size - 1, self.y + dy))

    def step(self, grid_size, others, foodweb, behavior, terrain=None):
        """In the simulation, animals generally move in a random pattern, but this behavior can be interrupted by behavior-based decisions. For example, if a predator detects nearby prey, it may switch from aimless wandering to purposeful pursuit. Likewise, a prey animal might abandon its random movement and start fleeing if it senses danger. This means that while randomness is the default, decision-making introduces more complex and natural movement patterns."""
        if not self.alive:
            return

        
        behavior.flee(self, others, foodweb)
        
        behavior.chase(self, others, foodweb)
       
        behavior.eat_if_possible(self, others, foodweb)

        behavior.random_move(self, grid_size, terrain)

        
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False

