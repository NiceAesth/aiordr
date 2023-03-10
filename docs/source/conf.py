# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import annotations

import os
import sys
from datetime import date

import toml

sys.path.insert(0, os.path.abspath("../../aiordr/"))

project = "aiordr"
author = "Nice Aesthetics"
project_copyright = f"{date.today().year}, {author}"
release = toml.load(os.path.abspath("../../pyproject.toml"))["tool"]["poetry"][
    "version"
]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]

autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
    "prev_next_buttons_location": None,
}
