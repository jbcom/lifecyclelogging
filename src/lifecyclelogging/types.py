"""Type definitions for the logging module."""

from __future__ import annotations

from typing import Literal

LogLevel = Literal["debug", "info", "warning", "error", "fatal", "critical"]
