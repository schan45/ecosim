# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- FIX: Add root project and package folder to sys.path --------------------
sys.path.insert(0, os.path.abspath('..'))              # project root
sys.path.insert(0, os.path.abspath('../ecosim'))       # package folder (adjust if named differently)

# -- Project information -----------------------------------------------------

project = 'ecosim'
copyright = '2025, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',     # include docstrings
    'sphinx.ext.napoleon',    # support NumPy/Google style docstrings
    'sphinx.ext.viewcode',    # link to source
    'sphinx.ext.githubpages', # support GitHub Pages
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Autodoc settings --------------------------------------------------------

autodoc_member_order = 'bysource'

# -- Napoleon settings -------------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
