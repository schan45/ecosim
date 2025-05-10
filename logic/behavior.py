import random
import math

def distance(a, b):
    """
    Calculate Manhattan distance between two animals.

    Parameters:
    a (Animal): First animal object with x and y coordinates.
    b (Animal): Second animal object with x and y coordinates.

    Returns:
    int: Manhattan distance between a and b.
    """
    return abs(a.x - b.x) + abs(a.y - b.y)

def random_move(animal, grid_size, terrain=None):
    """
    Move the animal to a random adjacent cell based on its speed.

    Parameters:
    animal (Animal): The animal object to move.
    grid_size (int): The size of the simulation grid.
    terrain (Terrain, optional): Terrain object for checking movement constraints.
    """
    if not animal.alive:
        return
    step_size = animal.speed
    if terrain and terrain.get_type(animal.x, animal.y) == "hill":
        step_size = 1

    tries = 0
    while tries < 10:
        dx = random.randint(-step_size, step_size)
        dy = random.randint(-step_size, step_size)
        new_x = max(0, min(animal.x + dx, grid_size - 1))
        new_y = max(0, min(animal.y + dy, grid_size - 1))
        if terrain and (terrain.is_blocked(new_x, new_y) or terrain.is_water(new_x, new_y)):
            tries += 1
            continue
        animal.x = new_x
        animal.y = new_y
        break

def chase(animal, others, foodweb, radius=3, terrain=None):
    """
    Chase the nearest prey within a radius if the animal has low energy.

    Parameters:
    animal (Animal): The predator trying to chase.
    others (list): List of other Animal objects in the grid.
    foodweb (FoodWeb): Object representing predator-prey relationships.
    radius (int, optional): Distance within which prey can be chased. Defaults to 3.
    terrain (Terrain, optional): Terrain object to validate movement.
    """
    if not animal.alive or animal.energy > 40:
        return

    prey_candidates = [
        other for other in others
        if foodweb.is_prey(animal.species, other.species)
        and other.alive and other != animal
        and distance(animal, other) <= radius
        and not (terrain and terrain.is_shelter(other.x, other.y))
    ]

    if prey_candidates:
        target = min(prey_candidates, key=lambda o: distance(animal, o))
        dx = int(math.copysign(1, target.x - animal.x)) if target.x != animal.x else 0
        dy = int(math.copysign(1, target.y - animal.y)) if target.y != animal.y else 0
        new_x = max(0, min(animal.x + dx, 19))
        new_y = max(0, min(animal.y + dy, 19))
        if terrain and (terrain.is_blocked(new_x, new_y) or terrain.is_water(new_x, new_y)):
            return
        animal.x = new_x
        animal.y = new_y
        animal.energy -= 1

def flee(animal, others, foodweb, terrain=None):
    """
    Move the animal away from nearby predators.

    Parameters:
    animal (Animal): The animal attempting to flee.
    others (list): List of other Animal objects in the grid.
    foodweb (FoodWeb): Object representing predator-prey relationships.
    terrain (Terrain, optional): Terrain object to validate movement.
    """
    predators = [
        other for other in others
        if foodweb.is_prey(other.species, animal.species)
        and other.alive and other != animal
        and distance(animal, other) <= 3
    ]
    if not predators:
        return

    avg_x = sum(p.x for p in predators) / len(predators)
    avg_y = sum(p.y for p in predators) / len(predators)
    dx = -1 if animal.x > avg_x else 1 if animal.x < avg_x else 0
    dy = -1 if animal.y > avg_y else 1 if animal.y < avg_y else 0
    new_x = max(0, min(animal.x + dx, 19))
    new_y = max(0, min(animal.y + dy, 19))
    if terrain and (terrain.is_blocked(new_x, new_y) or terrain.is_water(new_x, new_y)):
        return
    animal.x = new_x
    animal.y = new_y

def eat_if_possible(predator, others, foodweb):
    """
    Make the predator eat a prey at the same location if possible.

    Parameters:
    predator (Animal): The predator animal.
    others (list): List of other Animal objects.
    foodweb (FoodWeb): Object representing predator-prey relationships.
    """
    for prey in others:
        if prey.alive and prey.x == predator.x and prey.y == predator.y:
            if foodweb.is_prey(predator.species, prey.species):
                prey.alive = False
                predator.energy = min(predator.max_energy, predator.energy + 20)
