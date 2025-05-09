# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'ecosim'
copyright = '2025, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',    # automatically include docstrings
    'sphinx.ext.napoleon',   # support for NumPy/Google style docstrings
    'sphinx.ext.viewcode',   # add links to source code
    'sphinx.ext.githubpages' # support GitHub Pages
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Autodoc settings --------------------------------------------------------

autodoc_member_order = 'bysource'

# -- Napoleon settings (for NumPy/Google style docstrings) -------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
