from __future__ import annotations

import shutil
from pathlib import Path

import nox

# Configure nox
nox.options.sessions = ["tests", "lint", "type", "docs"]
nox.options.reuse_existing_virtualenvs = True

# Get Python versions from pyproject.toml classifiers
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]


def has_changes(session: nox.Session, *paths: str) -> bool:
    """Check if any files in given paths have changed."""
    if session.posargs and "--no-cached" in session.posargs:
        return True

    # Fallback to running everything if git not available
    try:
        output = session.run(
            "git", "rev-parse", "--verify", "HEAD", silent=True, success_codes=[0, 128]
        )
    except Exception:
        return True

    if output is None:  # No git
        return True

    try:
        session.run(
            "git", "diff-index", "--quiet", "HEAD", "--", *paths,
            success_codes=[0, 1], silent=True
        )
    except Exception:  # Changes detected
        return True

    return False


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
    """Run linting."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[dev]")

    # Only run if relevant files changed
    if has_changes(session, "src", "tests", "noxfile.py"):
        session.run("ruff", "format", "--check", ".")
        session.run("ruff", "check", ".")
    else:
        session.log("No changes detected in Python files, skipping lint")


@nox.session(python="3.12", venv_backend="uv")
def type(session: nox.Session) -> None:
    """Run type checking."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[dev]")

    # Only run if relevant files changed
    if has_changes(session, "src", "tests"):
        session.run("mypy", "src/lifecyclelogging")
        session.run("mypy", "tests")
    else:
        session.log("No changes detected in Python files, skipping type check")


@nox.session(python="3.12", venv_backend="uv")
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.install("--reinstall-package", "lifecyclelogging", "-e", ".[docs]")

    # Only rebuild if docs or source changed
    if has_changes(session, "docs", "src"):
        # Clean docs build
        build_dir = Path("docs") / "_build"
        if build_dir.exists():
            shutil.rmtree(build_dir)

        # Build docs
        session.run("sphinx-build", "-W", "docs", "docs/_build/html")
        session.run("sphinx-build", "-b", "linkcheck", "docs", "docs/_build/html")
    else:
        session.log("No changes detected in docs or source, skipping docs build")


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
