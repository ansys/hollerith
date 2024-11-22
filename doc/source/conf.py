"""Sphinx documentation configuration file."""
import os
from datetime import datetime

from sphinx.builders.latex import LaTeXBuilder

LaTeXBuilder.supported_image_types = ["image/png", "image/pdf", "image/svg+xml"]

from ansys_sphinx_theme import ansys_favicon, get_version_match, pyansys_logo_black
from hollerith import __version__

# Project information
project = "hollerith"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "Ansys Inc."
release = version = __version__

# use the default pyansys logo
cname = os.getenv("DOCUMENTATION_CNAME", default="hollerith.docs.pyansys.com")
switcher_version = get_version_match(version)
html_context = {
    "github_user": "ansys",
    "github_repo": "hollerith",
    "github_version": "main",
    "doc_path": "doc/source",
}
html_logo = pyansys_logo_black
html_favicon = ansys_favicon
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "Hollerith"

# specify the location of your github repo
html_theme_options = {
    "logo": "pyansys",
    "switcher": {
        "json_url": f"https://{cname}/versions.json",  # noqa: E231
        "version_match": switcher_version,
    },
    "check_switcher": False,
    "github_url": "https://github.com/ansys/hollerith",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True


# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}


# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

linkcheck_ignore = [
    "https://opensource.org/licenses/MIT",
]
