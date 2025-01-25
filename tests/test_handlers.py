"""Tests for logging handlers."""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from lifecyclelogging.handlers import add_console_handler, add_file_handler


def test_add_file_handler(tmp_path: Path) -> None:
    """Test adding a file handler."""
    logger = logging.getLogger("test_file")
    log_file = "test_file.log"

    with pytest.raises(RuntimeError, match="must contain at least one ASCII character"):
        add_file_handler(logger, "!@#$%^")

    add_file_handler(logger, log_file)
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)


def test_add_console_handler() -> None:
    """Test adding a console handler."""
    logger = logging.getLogger("test_console")
    add_console_handler(logger)
    assert len(logger.handlers) == 1
    assert logger.handlers[0].formatter is not None
