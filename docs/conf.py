# conf.py - Sphinx configuration for ReadTheDocs-compatible API docs

import os
import sys

sys.path.insert(0, os.path.abspath('..'))


project = 'Ecosim Toolbox'
copyright = '2025, Anna Schleier, Anikó Vitos, Tamás Bence Tóth'
author = 'Anna Schleier, Anikó Vitos, Tamás Bence Tóth'
release = '0.1'

extensions = [
    'myst_parser',              # to parse markdown
    'sphinx.ext.autodoc',       # <-- include docstrings
    'sphinx.ext.napoleon',      # <-- Google/NumPy docstring support
    'sphinx.ext.viewcode',      # <-- add [source] links
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Napoleon config for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Template and static paths
templates_path = ['_templates']
exclude_patterns = []

# HTML output config
html_theme = 'alabaster'  # or 'sphinx_rtd_theme' if installed

# Master doc (if not index.rst):
master_doc = 'index'

# Autodoc default options
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'inherited-members': True,
    'special-members': '__init__',
}

html_static_path = ['img']
html_logo = 'img/ecosim_logo.png'
html_theme_options = {
    'logo_name': True,
    'description': 'Ecosystem Simulation in Python',
    'github_user': 'schan45',
    'github_repo': 'ecosim',
    'fixed_sidebar': True,
    'page_width': '1024px',
    'sidebar_width': '220px',
    'body_text': '#333333',
    'sidebar_text': '#333333',
    'sidebar_background': '#fcdfb3',  # világos háttér
    'link': '#0066cc',
    'link_hover': '#004499',
}

html_css_files = ['custom.css']

autoclass_content = 'class'
autodoc_member_order = 'bysource'
