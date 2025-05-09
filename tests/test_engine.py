# tests/test_engine.py

import pytest
from simulation.engine import SimulationEngine
from simulation.organism import Organism

def test_simulation_initialization():
    engine = SimulationEngine()
    assert engine is not None
    assert isinstance(engine.organisms, list)

def test_simulation_step_advances_state():
    engine = SimulationEngine()
    initial_state = engine.get_state()
    engine.step()
    new_state = engine.get_state()
    assert initial_state != new_state

def test_organism_movement():
    engine = SimulationEngine()
    engine.step()
    for organism in engine.organisms:
        assert 0 <= organism.x < engine.grid_size
        assert 0 <= organism.y < engine.grid_size

def test_population_counts():
    engine = SimulationEngine()
    population = engine.get_population_counts()
    assert isinstance(population, dict)
    for species, count in population.items():
        assert isinstance(species, str)
        assert isinstance(count, int)
        assert count >= 0
