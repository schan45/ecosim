Welcome to ecosim's documentation!
==================================

**ecosim** is an ecological simulation toolbox designed to model and visualize interactions between producers and consumers in a grid-based environment.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   getting_started
   usage_guide
   usage

.. toctree::
   :maxdepth: 2
   :caption: Modules

   modules
   api

Installation
============

To install the project locally, clone the repository and run:

.. code-block:: bash

   git clone https://github.com/schan45/ecosim.git
   cd ecosim
   pip install -r requirements.txt

Example
=======

Here is an example Jupyter notebook you can run in Google Colab:

`Open in Google Colab <https://colab.research.google.com/drive/1x9O-ydAMVsbqQOgFuae_Nr9UdSIV2sac>`_

Features
========

- Grid-based ecological simulation
- Customizable terrain and species
- Population dynamics analysis
- Toolbox-like interface for user interaction

License
=======

This project is licensed under the MIT License. See the `LICENSE <https://github.com/schan45/ecosim/blob/main/LICENSE>`_ file for more details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

API Reference
=============

This section contains the automatically generated API reference for the **ecosim** toolbox.

Main Module
-----------
.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

Simulation Module
-----------------
.. automodule:: simulation
   :members:
   :undoc-members:
   :show-inheritance:

Terrain Module
--------------
.. automodule:: core.terrain
   :members:
   :undoc-members:
   :show-inheritance:

Organism Module
---------------
.. automodule:: core.organism
   :members:
   :undoc-members:
   :show-inheritance:

Utilities Module
----------------
.. automodule:: utils
   :members:
   :undoc-members:
   :show-inheritance:
