# GitHub Copilot Instructions for lifecyclelogging

## CI/CD Workflow - Read This First! 🚨

This repository uses a **unified CI workflow** in `.github/workflows/ci.yml`. This is an intentional design that:

### ✅ What is CORRECT (Do not suggest changing):

1. **No `[tool.semantic_release]` in pyproject.toml** - Configuration is in workflow YAML
2. **`commit: false`** - We don't want automated version bump commits
3. **`changelog: false`** - Changelogs are managed manually for better quality
4. **`push: false`** - Tags are already in GitHub, no need to push back
5. **`build: false`** - We use `hynek/build-and-inspect-python-package` instead

### ❌ Do NOT Suggest:

- Adding semantic-release config to pyproject.toml
- Splitting ci.yml into multiple workflow files
- Enabling automatic changelog generation
- Changing release workflow parameters
- "Fixing" the artifact download action versions (both v4 and v6 are intentional)

## Code Guidelines

### Imports
Always use extended-data-types utilities when available:
```python
# ✅ Good
from extended_data_types import (
    get_unique_signature,
    make_raw_data_export_safe,
    strtobool,
    strtopath,
)

# ❌ Avoid
def custom_str_to_bool(val): ...
```

### Type Hints
Use modern type hints:
```python
# ✅ Good
from collections.abc import Mapping
def func(data: Mapping[str, Any]) -> dict[str, Any]:

# ❌ Avoid
from typing import Dict
def func(data: Dict[str, Any]) -> Dict[str, Any]:
```

### Testing
- Always run tests locally before suggesting changes
- Maintain or improve test coverage
- Use pytest fixtures appropriately
- Test across Python 3.9-3.13

## Logging Best Practices

### Data Sanitization
Use `make_raw_data_export_safe` from extended-data-types:
```python
# ✅ Good
from extended_data_types import make_raw_data_export_safe
safe_data = make_raw_data_export_safe(data, export_to_yaml=False)

# ❌ Avoid custom sanitization
def my_sanitize(data): ...
```

### Path Handling
Use `strtopath` from extended-data-types:
```python
# ✅ Good
from extended_data_types import strtopath
path = strtopath(log_file_name)

# ❌ Avoid
from pathlib import Path
path = Path(log_file_name)
```

## Version Management

Version is defined in `src/lifecyclelogging/__init__.py`:
```python
__version__ = "0.1.3"
```

DO NOT suggest automated version bumping. Semantic-release reads this for version detection but does not write back to it.

## Questions?

See `AGENTS.md` for detailed explanations of our workflow design.
