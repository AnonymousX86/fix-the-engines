# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

from os import path as os_path
from sys import path as sys_path
sys_path.insert(0, os_path.abspath(os_path.join('..', '..')))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Fix The Engines'
copyright = '2024, Jakub Suchenek, Michał Gołębiewski'
author = 'Jakub Suchenek, Michał Gołębiewski'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Automatic documentation generation
    'sphinx.ext.viewcode'  # Link to local code
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Extension config --------------------------------------------------------

autodoc_default_options = {
    'members': True,  # Autodoc members
    'undoc-members': False,  # Autodoc undocumented memebers
    'private-members': True  # Autodoc private memebers
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['_static']
# html_sidebars = {
#     '**': ['search-field.html', 'sidebar-nav-bs.html'],
#     'index': []
#     }
# html_theme_options = {
#     'logo': {'text': project},
#     'navbar_end': ['theme-switcher', 'navbar-icon-links'],
#     'icon_links': [
#         {
#             'name': 'GitHub',
#             'url': 'https://github.com/AnonymousX86/fix-the-engines',
#             'icon': 'fa-brands fa-square-github',
#             'type': 'fontawesome'
#         }
#     ]
# }
