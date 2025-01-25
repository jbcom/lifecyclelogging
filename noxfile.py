"""Nox configuration for lifecyclelogging project."""

from __future__ import annotations

import shutil

from pathlib import Path

import nox


# Configure nox
nox.options.sessions = ["tests", "lint", "format", "type_check", "docs"]
nox.options.reuse_existing_virtualenvs = True

# Get Python versions from pyproject.toml classifiers
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_VERSIONS, venv_backend="uv", tags=["tests", "coverage"])
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.notify("coverage_report")
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[test]")

    session.run(
        "pytest",
        "tests",
        "--cov=lifecyclelogging",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-report=html",
        *session.posargs,
    )


@nox.session(python="3.12", venv_backend="uv")
def lint(session: nox.Session) -> None:
    """Run linting to check code quality."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[dev]")
    # Check for linting issues
    session.run("ruff", "check", ".")


@nox.session(python="3.12", venv_backend="uv")
def format_code(session: nox.Session) -> None:
    """Format code and sort imports."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[dev]")
    session.run("ruff", "check", "--fix", ".")


@nox.session(python="3.12", venv_backend="uv")
def type_check(session: nox.Session) -> None:
    """Run type checking."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[dev]")
    session.run("mypy", "src/lifecyclelogging")
    session.run("mypy", "tests")


@nox.session(python="3.12", venv_backend="uv")
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[docs]")

    # Clean docs build
    build_dir = Path("docs") / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # Build docs
    session.run("sphinx-build", "-W", "docs", "docs/_build/html", external=True)
    session.run(
        "sphinx-build", "-b", "linkcheck", "docs", "docs/_build/html", external=True
    )


@nox.session(python="3.12", venv_backend="uv")
def clean(session: nox.Session) -> None:
    """Clean build artifacts."""
    session.install("coverage[toml]")

    # Clean coverage
    session.run("coverage", "erase")

    # Clean build artifacts and caches
    patterns = [
        "build/",
        "dist/",
        "*.egg-info/",
        ".coverage*",
        "coverage.xml",
        "htmlcov/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".mypy_cache/",
        "docs/_build/",
    ]

    for pattern in patterns:
        for path in Path().glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


@nox.session(python="3.12", venv_backend="uv", tags=["coverage"])
def coverage_report(session: nox.Session) -> None:
    """Generate coverage report."""
    session.install("coverage[toml]")
    session.run("coverage", "combine", "--append", success_codes=[0, 1])
    session.run("coverage", "report")
    session.run("coverage", "html")
    session.run("coverage", "xml")
