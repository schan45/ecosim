Setup & Detailed Instructions
=============================

This page demonstrates the use of the ``ecosim2d`` ecosystem simulation package via a few steps. Make sure to follow the setup carefully to run simulations with custom terrain and food web configurations.

Step 1: Install the Package
---------------------------

.. code-block:: python

    !pip install ecosim2d

Step 2: Upload Input Files
--------------------------

Upload your config files to the Colab environment working directory:

- ``terrain_config.json``
- ``foodweb_config.json``

You can upload via the file browser or use:

.. code-block:: python

    from google.colab import files
    uploaded = files.upload()

You can also place them in a folder (``content/``) and refer using relative paths.

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
