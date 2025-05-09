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
    """Pl. fű, bokor – nem mozog, de 'élelmet' szolgáltat"""
    def __init__(self, species_name, x, y):
        super().__init__(species_name, x, y, energy=100)  # nem hal meg, default
        self.is_edible = True

    def step(self, grid_size):
        # Nem mozog, nem változik
        pass

# ----------------------------------------------------------------------------------

class Consumer(Organism):
    """Minden állat – mozgás, vadászat, menekülés stb."""
    def __init__(self, species_name, x, y, trophic_level='primary', speed=1):
        super().__init__(species_name, x, y, energy=100, max_energy=120)
        self.trophic_level = trophic_level
        self.speed = speed


    def move(self, grid_size):
        """Alap mozgás – véletlenszerű"""
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        self.x = max(0, min(grid_size - 1, self.x + dx))
        self.y = max(0, min(grid_size - 1, self.y + dy))

    def step(self, grid_size, others, foodweb, behavior, terrain=None):
        """Egy szimulációs lépés, viselkedésalapú döntéssel"""
        if not self.alive:
            return

        # 1. Menekülés, ha szükséges
        behavior.flee(self, others, foodweb)

        # 2. Zsákmány követése, ha van
        behavior.chase(self, others, foodweb)

        # 3. Evés, ha zsákmány van ugyanott
        behavior.eat_if_possible(self, others, foodweb)

        # 4. Ha nem történt elmozdulás (pl. nem volt veszély vagy cél)
        # akkor mozog véletlenszerűen
        behavior.random_move(self, grid_size, terrain)

        # Energiafogyasztás
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False

