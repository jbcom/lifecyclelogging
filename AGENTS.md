# AI Agent Guidelines for lifecyclelogging

This document provides critical context for AI coding assistants (Cursor, Codex, Copilot, Gemini, etc.) working on this repository.

## 🚨 CRITICAL: CI/CD Workflow Design Philosophy

### Our Unified CI Workflow Approach

**This repository uses a UNIFIED CI workflow** that combines testing, quality checks, AND release automation in a **single `ci.yml` file**. This is an INTENTIONAL design decision.

### Key Design Decisions (DO NOT SUGGEST CHANGING THESE)

#### 1. **Semantic Release Configuration - Hybrid Approach**

✅ **CORRECT Design:**
- `pyproject.toml` contains semantic-release configuration with `version_variables`
- The workflow uses these specific flags:
  ```yaml
  build: false          # We build with hynek/build-and-inspect-python-package
  vcs_release: true     # Create GitHub releases
  commit: false         # NO automatic commits
  tag: true             # Create version tags
  push: false           # Tags are pushed separately
  changelog: false      # NO automatic changelog commits
  ```

**WHY:**
- We use `hynek/build-and-inspect-python-package` for building (industry best practice)
- Semantic-release handles versioning and GitHub releases
- `version_variables` in pyproject.toml tells semantic-release to UPDATE version in source files
- With `commit: false`, the version update happens in-memory for the build, but isn't committed back
- We do NOT want automated changelog commits cluttering git history
- Manual changelog management provides better control and context

#### 2. **Version Variables Are REQUIRED**

The `pyproject.toml` file MUST contain:
```toml
[tool.semantic_release]
branch = "main"
allow_zero_version = false
version_variables = [
    "src/lifecyclelogging/__init__.py:__version__",
]
build_command = "python -m build"
upload_to_vcs_release = true
```

**WHY:**
- Without `version_variables`, semantic-release creates tags but doesn't update `__init__.py`
- The signed build step then builds with the OLD version from the source file
- This causes PyPI upload failures due to duplicate version numbers
- With `version_variables`, semantic-release updates the version in-memory before the build
- The workflow sets `commit: false` so these changes aren't committed back to git

#### 3. **The `push: false` Flag is CORRECT**

❌ **INCORRECT Agent Suggestion:**
> "Set `push: true` to push tags to remote"

✅ **CORRECT Design:**
- `push: false` is intentional
- The workflow runs on GitHub, tags are already in GitHub
- We don't need to push back to ourselves
- This prevents potential authentication issues

#### 4. **Artifact Download Versions**

Both `actions/download-artifact@v4` and `@v6` are acceptable:
- We use `@v6` for build artifacts in test jobs
- We use `@v4` for release artifacts (compatibility with signed builds)
- This is NOT a mistake or inconsistency
- DO NOT suggest "fixing" this

### What This Workflow DOES

```
On Push to main:
  ↓
1. Build & verify package ✓
  ↓
2. Run tests across all Python versions ✓
  ↓
3. Type checking with pyright ✓
  ↓
4. Linting with pre-commit ✓
  ↓
5. Generate coverage report ✓
  ↓
6. IF all pass → Semantic Release:
   - Analyze commit messages
   - Determine next version
   - Create Git tag
   - Create GitHub release
   ↓
7. Build signed attestation ✓
  ↓
8. Publish to PyPI ✓
```

### What This Workflow DOES NOT DO

❌ Create changelog commits
❌ Commit version bumps back to repository (updates happen in-memory for build only)
❌ Use multiple workflow files
❌ Push tags back to GitHub (they're already there)

## 📝 Making Code Changes

### When Reviewing PRs

**DO:**
- ✅ Review code quality and correctness
- ✅ Check test coverage
- ✅ Verify type hints
- ✅ Suggest API improvements
- ✅ Check for security issues

**DO NOT:**
- ❌ Suggest adding semantic-release config to pyproject.toml
- ❌ Recommend splitting ci.yml back into multiple files
- ❌ Suggest automated changelog generation
- ❌ Recommend changing release workflow parameters
- ❌ Flag the unified workflow as "incorrect" or "missing configuration"

### Understanding Version Management

```
Version Source: src/lifecyclelogging/__init__.py
   ↓
__version__ = "0.1.3"
   ↓
Read by: hatchling (setuptools backend)
   ↓
Used by: semantic-release for version detection
   ↓
Tag Created: v0.1.3 (or next version based on commits)
   ↓
Published to: PyPI with that version
```

**We do NOT:**
- ❌ Have semantic-release auto-increment `__version__` in files
- ❌ Commit version changes back to repository
- ❌ Use version_tostring or version_variable in semantic-release config

### Commit Message Format

We follow conventional commits:
- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Test improvements
- `ci:` - CI/CD changes

**Breaking changes:**
- Add `BREAKING CHANGE:` in commit body for major version bumps
- Or use `feat!:` / `fix!:` notation

## 🔧 Development Workflow

### Local Development

```bash
# Install dependencies
pip install -e ".[tests,typing,docs]"

# Run tests
pytest

# Run type checking
mypy src/

# Run linting
pre-commit run --all-files
```

### Creating PRs

1. Create a feature branch
2. Make your changes
3. Run tests locally
4. Create PR against `main`
5. CI will run automatically
6. Merge to main when approved

### Releases (Automated)

When PR is merged to main:
1. CI runs all checks
2. Semantic-release analyzes commits since last tag
3. If release needed:
   - Creates version tag
   - Creates GitHub release
   - Builds signed package
   - Publishes to PyPI
4. **NO commits are made to the repository**

## 🎯 Common Agent Misconceptions

### Misconception #1: "Can skip semantic-release config"

**Agent says:** "All semantic-release configuration can be done via workflow parameters"

**Reality:** The `version_variables` configuration MUST be in pyproject.toml. Without it, semantic-release won't update the version in source files, causing the build to use stale version numbers.

### Misconception #2: "Workflow will fail without config"

**Agent says:** "The release job will likely fail without semantic-release config"

**Reality:** The workflow has successfully run hundreds of times across our repositories. It works as designed.

### Misconception #3: "Need to add changelog configuration"

**Agent says:** "Enable changelog: true for automated changelog updates"

**Reality:** We intentionally set `changelog: false` because we maintain changelogs manually for better quality and context.

### Misconception #4: "Version variables are optional"

**Agent says:** "Version variables aren't needed since we have commit: false"

**Reality:** Version variables ARE REQUIRED! They tell semantic-release to update `__version__` in-memory before building. Without them, the build uses the old version from disk, causing duplicate version uploads to PyPI. With `commit: false`, the update happens only in the working tree and isn't committed back to git.

### Misconception #5: "Multiple files better"

**Agent says:** "Consider splitting ci.yml and release.yml for separation of concerns"

**Reality:** We INTENTIONALLY unified them. This is the modern pattern we're adopting across all repos.

## 📚 Reference Implementation

This workflow design is based on:
- ✅ extended-data-types (the parent library)
- ✅ hynek/build-and-inspect-python-package best practices
- ✅ Python Packaging Authority recommendations
- ✅ Trusted publishing to PyPI (no tokens needed)

## 🤝 Getting Help

If you're an AI agent uncertain about a suggestion:
1. Check this document first
2. Look at the extended-data-types repository for reference
3. When in doubt, DO NOT suggest changes to the CI workflow
4. Focus on code quality, tests, and documentation

---

**Last Updated:** 2025-11-24
**Workflow Version:** Unified CI v1.0 (python-semantic-release@v9.17.0)
