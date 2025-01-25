"""Handlers for different logging outputs."""

from __future__ import annotations

import logging
import re

from rich.logging import RichHandler


def add_file_handler(logger: logging.Logger, log_file_name: str) -> None:
    """Adds a file handler to the logger, sanitizing the file name."""
    sanitized_name = re.sub(r"[^0-9a-zA-Z]+", "_", log_file_name.rstrip(".log"))
    if not sanitized_name[:1].isalnum():
        first_alpha = re.search(r"[A-Za-z0-9]", sanitized_name)
        if not first_alpha:
            raise RuntimeError(
                f"Malformed log file name: {sanitized_name} must contain at least one ASCII character",
            )
        sanitized_name = sanitized_name[first_alpha.start():]

    log_file = f"{sanitized_name}.log"
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        "[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def add_console_handler(logger: logging.Logger) -> None:
    """Adds a Rich console handler to the logger."""
    console_handler = RichHandler(rich_tracebacks=True)
    console_formatter = logging.Formatter("%(message)s", datefmt="[%X]")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
