# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime

from czml3 import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "czml3"
copyright = f"{datetime.datetime.now().year}, Daniel Stoops"
author = "Daniel Stoops"
release = f"v{__version__}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": ["globaltoc.html", "relations.html", "sourcelink.html", "searchbox.html"]
}
# html_favicon = ""
