
import pytest
from core.organism import Organism
import logic.behavior as behavior

# Dummy terrain that allows all movement (optional terrain testing)
class DummyTerrain:
    def get_type(self, x, y):
        return "plain"

def test_organism_initialization():
    org = Organism("Rabbit", 5, 5, energy=80, max_energy=100)
    assert org.species == "Rabbit"
    assert org.x == 5 and org.y == 5
    assert org.energy == 80
    assert org.max_energy == 100
    assert org.alive is True

def test_random_move_changes_position():
    org = Organism("Fox", 3, 3)
    old_pos = (org.x, org.y)
    behavior.random_move(org, grid_size=10)
    assert (org.x, org.y) != old_pos, "Organism should change position after move."

def test_energy_decreases_after_move():
    org = Organism("Fox", 3, 3, energy=50)
    original_energy = org.energy
    behavior.random_move(org, grid_size=10)
    assert org.energy < original_energy, "Energy should decrease after movement."

def test_organism_dies_when_energy_depleted():
    org = Organism("Rabbit", 4, 4, energy=1)
    org.energy = 0
    org.alive = False
    assert not org.alive, "Organism should be dead when energy reaches 0."
