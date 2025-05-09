
import random
import math

def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def random_move(animal, grid_size, terrain=None):
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
    for prey in others:
        if prey.alive and prey.x == predator.x and prey.y == predator.y:
            if foodweb.is_prey(predator.species, prey.species):
                prey.alive = False
                predator.energy = min(predator.max_energy, predator.energy + 20)
