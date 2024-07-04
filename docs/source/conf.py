# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MECAnywhere'
copyright = '2024, Junxue'
author = 'Junxue'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
   'myst_parser',
   'sphinx_rtd_theme',
   'sphinxcontrib.openapi',
   'sphinxcontrib.redoc',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


redoc = [
    {
        'name': 'Pymeca Actors Server API',
        'page': 'pages/api/pymeca-actors-server-api',
        'spec': '../../pymeca-actors/src/openapi.json',
        'embed': True,
    },
    {
        'name': 'Tower API',
        'page': 'pages/api/tower-api',
        'spec': '../../tower/src/openapi.json',
        'embed': True,
    }
]

redoc_uri = "https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"
