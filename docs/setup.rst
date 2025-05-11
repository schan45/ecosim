Setup & Detailed Instructions
=============================

This page demonstrates the use of the ``ecosim2d`` ecosystem simulation package via a few steps. Make sure to follow the setup carefully to run simulations with custom terrain and food web configurations.

Step 1: Install the Package
---------------------------

.. code-block:: python

    !pip install ecosim2d

Step 2: Upload Input Files
--------------------------

Ecosim uses two main configuration files as input to define the ecosystem's species and environment:

1. ``foodweb_config.json`` – defines organisms, their types, and predator-prey relationships.
2. ``terrain_config.json`` – describes the spatial layout of environmental features like trees, water, and shelters.

Both JSON files must be present in the working directory or referenced with correct relative paths in simulation parameters.

foodweb_config.json
-------------------

This file defines the biological entities and feeding relationships within the ecosystem.

Example:

.. code-block:: json

    {
      "organisms": {
        "Carrot": {
          "type": "Producer",
          "color": "#fa7b05",
          "initial_count": 20
        },
        "Rabbit": {
          "type": "Consumer",
          "trophic_level": "primary",
          "color": "#85807e",
          "initial_count": 15
        },
        "Fox": {
          "type": "Consumer",
          "trophic_level": "secondary",
          "color": "#eb0505",
          "initial_count": 7
        },
        "Fungi": {
          "type": "Decomposer",
          "decomposition_rate": 3
        }
      },
      "predation": {
        "Rabbit": ["Carrot"],
        "Fox": ["Rabbit"]
      }
    }

**Structure Details:**

* ``organisms`` – a dictionary where each key is a species name.
  * Each species includes:
    * ``type``: "Producer", "Consumer", or "Decomposer"
    * ``trophic_level`` (optional for Consumers): "primary", "secondary", etc.
    * ``color``: Hex code for visual representation
    * ``initial_count``: Number of individuals at simulation start
    * ``decomposition_rate``: (only for Decomposers) optional numeric rate

* ``predation`` – defines the food web in key-value format, where each consumer species maps to a list of prey species.

terrain_config.json
-------------------

This file defines how terrain features are arranged in the simulation grid.

Ecosim supports two terrain modes: ``manual`` and ``random``.

**Manual terrain mode** allows explicit placement of objects:

.. code-block:: json

    {
      "mode": "manual",
      "terrain_objects": [
        { "type": "water", "x": 3, "y": 3, "width": 4, "height": 2 },
        { "type": "hill", "x": 10, "y": 10, "width": 3, "height": 3 },
        { "type": "tree", "x": 5, "y": 5 },
        { "type": "shelter", "x": 15, "y": 6 }
      ]
    }

**Supported terrain types** include:

* ``water`` – blocks movement, animals can drink here and gain energy
* ``tree`` – blocks movement
* ``hill`` – increases movement cost
* ``shelter`` – offers protection from threats for primary consumers

Each object must specify ``x`` and ``y`` coordinates. Optionally, use ``width`` and ``height`` for rectangular regions.

**Random terrain mode** disables manual placement and uses random generation logic (if supported):

.. code-block:: json

    {
      "mode": "random"
    }

⚠️ *Note:* The mode key must be spelled correctly – avoid typos like "radnom".

File Placement and Usage
------------------------

Both configuration files must be referenced in the simulation function:

.. code-block:: python

    simulation(
        grid_size=20,
        steps=30,
        terrain_config_path="content/terrain_config.json",
        foodweb_config_path="content/foodweb_config.json"
    )

Make sure the file paths are correct relative to the working directory (e.g., `/content/` in Google Colab).

``foodweb_config.json`` and ``terrain_config.json`` define the biological logic and spatial environment that drive all simulation behavior.


Step 3: Run Simulation
----------------------

Import the simulation entry function and run it with parameters:

.. code-block:: python

    from mainsimulation.main import simulation

    # Run with custom settings
    simulation(grid_size=20, steps=5,
               terrain_config_path="content/terrain_config.json",
               foodweb_config_path="content/foodweb_config.json")

Step 4: Output Location
-----------------------

- Visual frames: ``frames/`` folder
- Heatmaps: ``statistics_plots/heatmap_*.png``
- Population chart: ``statistics_plots/population_chart.png``

Download outputs:

.. code-block:: python

    from google.colab import files
    files.download('statistics_plots/population_chart.png')

----

This guide assumes the ``ecosim2d`` package handles all I/O via relative paths from the notebook's working directory (``/content/``). Ensure your simulation module supports these file paths dynamically.
