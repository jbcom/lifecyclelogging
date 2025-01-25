"""Utility functions for logging configuration."""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from copy import copy, deepcopy
from typing import Any

from extended_data_types import wrap_raw_data_for_export

from .const import DEFAULT_LOG_LEVEL


def get_log_level(level: int | str) -> int:
    """Converts a log level from string or integer to a logging level integer."""
    if isinstance(level, str):
        return logging._nameToLevel.get(level.upper(), DEFAULT_LOG_LEVEL)  # type: ignore[attr-defined]
    return level if level in logging._levelToName else DEFAULT_LOG_LEVEL  # type: ignore[attr-defined]


def get_loggers() -> list[logging.Logger]:
    """Retrieves all active loggers."""
    loggers = [logging.getLogger()]
    loggers.extend(logging.getLogger(name) for name in logging.root.manager.loggerDict)
    return loggers


def find_logger(name: str) -> logging.Logger | None:
    """Finds a logger by its name."""
    for logger in get_loggers():
        if logger.name == name:
            return logger
    return None


def clear_existing_handlers(logger: logging.Logger) -> None:
    """Removes all existing handlers from the logger."""
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def sanitize_json_data(data: Any) -> Any:
    """Sanitize data for JSON serialization."""
    if isinstance(data, (bool, str, type(None))):
        return data
    if isinstance(data, (int, float)):
        try:
            if abs(data) > 2 ** 53:
                return str(data)
        except OverflowError:
            return str(data)
        return data
    if isinstance(data, dict):
        return {
            str(k): sanitize_json_data(v)
            for k, v in data.items()
        }
    if isinstance(data, (list, tuple)):
        return [sanitize_json_data(v) for v in data]
    return str(data)


def add_labeled_json(
        msg: str,
        labeled_data: Mapping[str, Mapping[str, Any]],
) -> str:
    """Add labeled JSON data to the message."""
    for label, jd in deepcopy(labeled_data).items():
        if not isinstance(jd, Mapping):
            jd = {label: jd}
            msg += "\n:" + wrap_raw_data_for_export(
                sanitize_json_data(jd),
                allow_encoding=True,
            )
            continue

        msg += f"\n{label}:\n" + wrap_raw_data_for_export(
            sanitize_json_data(jd),
            allow_encoding=True,
        )
    return msg


def add_unlabeled_json(
        msg: str,
        json_data: Mapping[str, Any] | Sequence[Mapping[str, Any]],
) -> str:
    """Add unlabeled JSON data to the message."""
    unlabeled_json_data = (
        deepcopy(json_data)
        if isinstance(json_data, Sequence)
        else [copy(json_data)]
    )

    for jd in unlabeled_json_data:
        msg += "\n:" + wrap_raw_data_for_export(
            sanitize_json_data(jd),
            allow_encoding=True,
        )
    return msg


def add_json_data(
        msg: str,
        json_data: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None,
        labeled_json_data: Mapping[str, Mapping[str, Any]] | None,
) -> str:
    """Add JSON data to the log message."""
    if labeled_json_data:
        msg = add_labeled_json(msg, labeled_json_data)

    if json_data:
        msg = add_unlabeled_json(msg, json_data)

    return msg
