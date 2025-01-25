"""Tests for utility functions."""
from __future__ import annotations

import logging
from typing import Any

import pytest

from lifecyclelogging.utils import (
    get_log_level,
    get_loggers,
    find_logger,
    clear_existing_handlers,
    sanitize_json_data,
)


def test_get_log_level() -> None:
    """Test log level conversion."""
    assert get_log_level("DEBUG") == logging.DEBUG
    assert get_log_level("info") == logging.INFO
    assert get_log_level(logging.WARNING) == logging.WARNING
    assert get_log_level("INVALID") == logging.DEBUG  # Default


def test_get_loggers() -> None:
    """Test retrieving all loggers."""
    loggers = get_loggers()
    assert len(loggers) > 0
    assert all(isinstance(logger, logging.Logger) for logger in loggers)


def test_find_logger() -> None:
    """Test finding a logger by name."""
    test_logger = logging.getLogger("test_find")
    found_logger = find_logger("test_find")
    assert found_logger is test_logger
    assert find_logger("nonexistent") is None


def test_clear_existing_handlers() -> None:
    """Test clearing logger handlers."""
    logger = logging.getLogger("test_clear")
    logger.addHandler(logging.NullHandler())
    assert len(logger.handlers) > 0

    clear_existing_handlers(logger)
    assert len(logger.handlers) == 0


@pytest.mark.parametrize("input_data,expected", [
    (123, 123),
    (2 ** 60, str(2 ** 60)),  # Large int becomes string
    ({"key": 123}, {"key": 123}),
    ({"key": 2 ** 60}, {"key": str(2 ** 60)}),
    ([1, 2 ** 60, "test"], [1, str(2 ** 60), "test"]),
    (complex(1, 2), str(complex(1, 2))),  # Non-JSON type becomes string
])
def test_sanitize_json_data(input_data: Any, expected: Any) -> None:
    """Test JSON data sanitization."""
    assert sanitize_json_data(input_data) == expected
