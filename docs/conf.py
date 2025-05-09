# -*- coding: utf-8 -*-

# -- Path setup --------------------------------------------------------------

import os
import sys

# Add your project's directories to sys.path for autodoc
sys.path.insert(0, os.path.abspath(".."))        # main project root
sys.path.insert(0, os.path.abspath("../core"))   # example module
sys.path.insert(0, os.path.abspath("../logic"))
sys.path.insert(0, os.path.abspath("../simulation"))

# -- Project information -----------------------------------------------------

project = 'Ecosim'
copyright = '2025, Your Name or Team'
author = 'Your Name or Team'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

autoclass_content = "both"

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # if you use Google/Numpy style docstrings
    'nbsphinx',
]

templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None
todo_include_todos = True
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
}

# Optional: logo path (comment out if unused)
# html_logo = "logo.png"

# -- Static files ------------------------------------------------------------

html_static_path = ['_static']

# -- Output file names -------------------------------------------------------

htmlhelp_basename = 'EcosimDoc'

latex_documents = [
    (master_doc, 'Ecosim.tex', 'Ecosim Documentation',
     author, 'manual'),
]

man_pages = [
    (master_doc, 'ecosim', 'Ecosim Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'Ecosim', 'Ecosim Documentation',
     author, 'Ecosim', 'Ecological simulation toolkit.',
     'Miscellaneous'),
]

epub_title = project
epub_exclude_files = ['search.html']
