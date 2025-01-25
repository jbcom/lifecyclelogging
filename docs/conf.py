from __future__ import annotations

import os


project = "LifecycleLogging"
author = "Jon Bogaty"
copyright_notice = f"2025, {author}"
version = "0.1.0"

extensions = [
    "autodoc2",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
]

autodoc2_packages = [
    {
        "path": "../src/lifecyclelogging",
    }
]

default_role = "any"

autodoc_typehints = "description"
autodoc_typehints_format = "fully-qualified"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "sphinx_rtd_theme"

html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    # Special handling when building on Read the Docs
    html_context["READTHEDOCS"] = True
else:
    # If building locally or on GitHub Pages
    html_context.update(
        {
            "display_github": True,
            "github_user": "user",
            "github_repo": "lifecyclelogging",
            "github_version": "main",
        }
    )

nitpick_ignore = []
nitpick_ignore_regex = []
