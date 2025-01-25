"""Common test fixtures."""
from __future__ import annotations

import pytest

from lifecyclelogging import Logging


@pytest.fixture
def logger() -> Logging:
    """Create a logger instance for testing."""
    return Logging(enable_console=False, enable_file=False)
