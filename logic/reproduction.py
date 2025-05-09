from collections import defaultdict, Counter
from core.organism import Producer, Consumer
import random

REPRO_COOLDOWN_BY_LEVEL = {
    "primary": 2,
    "secondary": 6,
    "tertiary": 8,
    "omnivore": 5,
    "unknown": 5
}

REPRO_ENERGY_THRESHOLD_BY_LEVEL = {
    "primary": 60,
    "secondary": 80,
    "tertiary": 90,
    "omnivore": 70,
    "unknown": 80
}

REPRO_RATIOS = {
    "Rabbit": 2,   # 1 Rabbit -> 2 Carrot
    "Fox": 1       # 1 Fox -> 1 Rabbit
}

def reproduce(organisms, grid_size, step_counter):
    new_organisms = []
    species_by_pos = defaultdict(list)

    for org in organisms:
        if org.alive:
            species_by_pos[(org.x, org.y)].append(org)

    live_counts = Counter([o.species for o in organisms if o.alive])
    food_sources = defaultdict(int)

    if hasattr(reproduce, "_foodweb") and reproduce._foodweb:
        fw = reproduce._foodweb
        for species in live_counts:
            prey_species = fw.get_prey(species)
            total_prey = sum(live_counts[prey] for prey in prey_species)
            food_sources[species] = total_prey

    # --- Producer Respawn ---
    if step_counter % 30 == 0:
        producer_species = set(o.species for o in organisms if isinstance(o, Producer))
        producers_alive = any(isinstance(o, Producer) and o.alive for o in organisms)

        if not producers_alive:
            for species in producer_species:
                for _ in range(3):
                    new_x = random.randint(0, grid_size - 1)
                    new_y = random.randint(0, grid_size - 1)
                    if any(o.x == new_x and o.y == new_y and o.alive for o in organisms):
                        continue
                    if hasattr(reproduce, "_terrain") and reproduce._terrain.is_blocked(new_x, new_y):
                        continue
                    new_organisms.append(Producer(species, new_x, new_y))
        else:
            for org in organisms:
                if isinstance(org, Producer) and org.alive:
                    dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                    new_x = min(grid_size - 1, max(0, org.x + dx))
                    new_y = min(grid_size - 1, max(0, org.y + dy))
                    if any(o.x == new_x and o.y == new_y and o.alive for o in organisms):
                        continue
                    if hasattr(reproduce, "_terrain") and (
                        reproduce._terrain.is_blocked(new_x, new_y)
                        or reproduce._terrain.is_water(new_x, new_y)
                        or reproduce._terrain.is_shelter(new_x, new_y)):
                        continue
                    new_organisms.append(Producer(org.species, new_x, new_y))

    # --- Consumer on same cell ---
    for pos, orgs in species_by_pos.items():
        groups = defaultdict(list)
        for o in orgs:
            if isinstance(o, Consumer):
                groups[o.species].append(o)

        for species, members in groups.items():
            if len(members) < 2:
                continue
            if not all(m.energy >= REPRO_ENERGY_THRESHOLD_BY_LEVEL.get(m.trophic_level, 70) for m in members):
                continue

            prey_available = food_sources.get(species, 0)
            current = live_counts[species]
            required_ratio = REPRO_RATIOS.get(species, 1)
            if prey_available / required_ratio < current:
                continue

            last = reproduce._last_repro.get((species, pos), -999)
            cooldown = REPRO_COOLDOWN_BY_LEVEL.get(members[0].trophic_level, 5)
            if step_counter - last >= cooldown:
                new_organisms.append(Consumer(species, pos[0], pos[1], trophic_level=members[0].trophic_level))
                reproduce._last_repro[(species, pos)] = step_counter

    # --- Consumer proximity based (all consumers including primary) ---
    paired = set()
    consumers = [o for o in organisms if isinstance(o, Consumer)]
    for i, o1 in enumerate(consumers):
        for o2 in consumers[i+1:]:
            if o1.species != o2.species or id(o1) in paired or id(o2) in paired:
                continue
            if abs(o1.x - o2.x) + abs(o1.y - o2.y) == 2:
                if o1.energy >= 40 and o2.energy >= 40:
                    avg_x = (o1.x + o2.x) // 2
                    avg_y = (o1.y + o2.y) // 2
                    if hasattr(reproduce, "_terrain") and (
                        reproduce._terrain.is_blocked(avg_x, avg_y)
                        or reproduce._terrain.is_water(avg_x, avg_y)):
                        continue
                    prey_available = food_sources.get(o1.species, 0)
                    predatorcount = live_counts.get(o1.species, 0)
                    current = live_counts[o1.species]
                    required_ratio = REPRO_RATIOS.get(o1.species, 1)
                    if prey_available <= predatorcount*2:
                        continue
                    if prey_available / required_ratio < current:
                        if random.random() > 0.7:
                            continue
                    pos = (avg_x, avg_y)
                    last = reproduce._last_repro.get((o1.species, pos), -999)
                    cooldown = REPRO_COOLDOWN_BY_LEVEL.get(o1.trophic_level, 5)
                    if step_counter - last >= cooldown:
                        new_organisms.append(Consumer(o1.species, avg_x, avg_y, trophic_level=o1.trophic_level))
                        reproduce._last_repro[(o1.species, pos)] = step_counter
                        paired.add(id(o1))
                        paired.add(id(o2))

    # --- Primary 1 remaining fallback to shelter ---
    if hasattr(reproduce, "_foodweb") and reproduce._foodweb:
        fw = reproduce._foodweb
        for species, count in live_counts.items():
            if count == 1 and fw.get_trophic_level(species) == "primary":
                last = reproduce._last_primary_respawn.get(species, -999)
                if step_counter - last >= 2:
                    if hasattr(reproduce, "_terrain"):
                        for (x, y), t in reproduce._terrain.map.items():
                            if t == "shelter":
                                new_organisms.append(Consumer(species, x, y, trophic_level="primary"))
                                reproduce._last_primary_respawn[species] = step_counter
                                break

    return new_organisms

reproduce._last_repro = {}
reproduce._last_primary_respawn = {}
reproduce._foodweb = None
reproduce._terrain = None
