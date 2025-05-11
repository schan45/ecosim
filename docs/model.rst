Model Capabilities
==================

This section explains the core capabilities of the simulation toolbox. It helps users understand how the model works, what inputs are needed, and how flexible the ecosystem simulation can be.

Defining Species in the Food Web
--------------------------------

The simulation can include multiple species — both producers (like plants) and consumers (like herbivores, predators).

Each species must have a unique name and assigned type:

  * ``Producer`` (e.g., Carrot)
  * ``Consumer`` (e.g., Rabbit, Fox)

Each species is defined in the ``foodweb.json`` configuration file and must include:

* A unique name
* A type: ``Producer`` or ``Consumer``
* An optional trophic level for consumers: ``primary``, ``secondary``, ``tertiary``, or ``omnivore``
* A color to represent the species visually on the simulation grid

Predator–Prey Relations
-----------------------

You can define who eats whom using a predator-prey matrix.

* For example, a ``Fox`` may be defined to eat ``Rabbit``, and ``Rabbit`` may eat ``Carrot``.

* These relations are also stored in the ``foodweb_config.json``.

This structure defines the energy flow and food chain behavior during the simulation.

The ``foodweb.py`` file handles the definition and relationships of species in the ecosystem simulation. It loads information from a JSON configuration file (usually ``foodweb_config.json``) and provides helper functions to access species traits and interactions.

Animal Behaviours
-----------------

In the simulation, animal agents (Consumers) exhibit goal-oriented and dynamic behaviors driven by their type and environment. These behaviors are defined in the ``organism.py`` file, specifically in the ``Consumer`` class.

Key behaviors include:

* **Movement**:  
  Animals can move across the grid each simulation step. By default, movement is random, but it can be influenced by terrain and nearby prey.

* **Hunting & Feeding**:  
  Consumers check their surroundings for edible species based on the food web. If prey is found nearby, the animal may move toward it and consume it.

* **Survival Logic**:  
  Animals track their state — whether they are alive, have eaten, or are blocked by obstacles. Dead organisms are excluded from later steps.

* **Optional Tracking**:  
  Consumers may also track:
  
  * Total distance traveled
  * Number of successful hunts or meals
  * Reproductive state or energy level (if extended)

These behaviors are executed during each simulation step via the ``step()`` method, which is called on every living consumer.

Spatial Complexity: Map and Terrain
-----------------------------------

The ``terrain.py`` file defines the environmental layout of the simulation world. It controls how different terrain types affect the behavior and survival of organisms.

Each grid cell can be assigned a terrain type, such as:

* **Plain** – default walkable ground
* **Water** – impassable; organisms cannot enter
* **Tree** – walkable or blocked depending on rules
* **Hill** – may affect movement or strategy
* **Shelter** – can protect organisms from threats

The terrain system offers several important functionalities that shape how organisms interact with their environment:

* **Terrain Generation**:  
  The terrain is initialized as a grid loaded from predefined logic. This sets the simulation’s physical environment.

* **Interaction Logic**:  
  Methods such as ``is_water(x, y)`` or ``is_blocked(x, y)`` allow organisms to check if a grid cell is passable.

* **Environmental Effects**:  
  The terrain can apply effects each simulation step, for example:

  * Reducing energy
  * Offering shelter
  * Preventing reproduction or movement

* **Shelter System**:  
  Special updates are applied to shelter cells (e.g., rotating availability or hiding capacity).

Temporal Depth (Steps)
-----------------------

The simulation runs for a specified number of steps.

* Each step represents a discrete time unit (e.g., one turn).

* During each step:

  * Organisms move, eat, reproduce, and possibly die.
  * New organisms may be born, heatmaps and population logs are updated.

You can control the number of steps via the ``steps`` parameter when initializing the engine.
