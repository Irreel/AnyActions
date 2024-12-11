# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'AnyActions'
copyright = '2024, Anthea Zhao'
author = ['Anthea Zhao', 'Ziang Tong']
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",       # Required for documenting Python code
    "sphinx.ext.napoleon",      # If using Google/NumPy-style docstrings
    "sphinx_autodoc_typehints", # Automatically document type hints
    "sphinx.ext.coverage", # Check for the documentation coverage
    "sphinx.ext.autosummary"
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
