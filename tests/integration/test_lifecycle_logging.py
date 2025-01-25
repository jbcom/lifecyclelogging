from __future__ import annotations

from pathlib import Path

import pytest

from lifecyclelogging import Logging


@pytest.fixture
def temp_logger(tmp_path: Path) -> Logging:
    """Create a logger instance with file output for integration testing."""
    return Logging(
        enable_file=True,
        log_file_name="test_app.log",
        logger_name="integration_test"
    )


def test_full_logging_lifecycle(temp_logger: Logging, tmp_path: Path) -> None:
    """Test the complete lifecycle of logging with file output."""
    # Test basic message
    basic_msg = "Basic message"
    basic_result = temp_logger.logged_statement(
        basic_msg,
        log_level="info",  # type: ignore[arg-type]
    )
    assert basic_result == basic_msg

    # Test with context marker
    context_msg = "Context message"
    context_result = temp_logger.logged_statement(
        context_msg,
        context_marker="test_context",
        log_level="info",  # type: ignore[arg-type]
    )
    assert "[test_context]" in context_result

    # Test with storage marker
    storage_msg = "Storage message"
    storage_marker = "test_storage"
    storage_result = temp_logger.logged_statement(
        storage_msg,
        storage_marker=storage_marker,
        log_level="info",  # type: ignore[arg-type]
    )
    assert storage_result is not None
    assert storage_msg in temp_logger.stored_messages[storage_marker]

    # Verify file output
    log_path = tmp_path / "test_app.log"
    assert log_path.exists()
    log_content = log_path.read_text()

    assert basic_msg in log_content
    assert context_msg in log_content
    assert storage_msg in log_content


def test_verbosity_integration(temp_logger: Logging) -> None:
    """Test verbosity controls in an integrated way."""
    temp_logger.enable_verbose_output = True
    temp_logger.verbosity_threshold = 2

    messages = [
        (1, "Normal verbosity"),
        (2, "High verbosity"),
        (3, "Excessive verbosity"),
    ]

    for verbosity, msg in messages:
        result = temp_logger.logged_statement(
            msg,
            verbose=True,
            verbosity=verbosity,
            log_level="debug",  # type: ignore[arg-type]
        )

        if verbosity <= temp_logger.verbosity_threshold:
            assert result == msg
        else:
            assert result is None


def test_marker_integration(temp_logger: Logging) -> None:
    """Test both marker systems working together."""
    context_marker = "context_test"
    storage_marker = "storage_test"

    # Add as verbosity bypass
    temp_logger.verbosity_bypass_markers.append(context_marker)

    # Even with verbose=True and verbosity=5, should appear due to bypass
    msg = "Test message"
    result = temp_logger.logged_statement(
        msg,
        context_marker=context_marker,
        storage_marker=storage_marker,
        verbose=True,
        verbosity=5,
        log_level="debug",  # type: ignore[arg-type]
    )

    assert result is not None
    assert f"[{context_marker}]" in result
    assert msg in next(iter(temp_logger.stored_messages[storage_marker]))
