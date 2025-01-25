# LifecycleLogging

A flexible and extensible logging utility for Python projects, combining the power of `logging` and `rich` to handle file and console outputs seamlessly.

## Installation

Install LifecycleLogging using `pip`:

```bash
pip install lifecyclelogging
```

## Features

- Flexible logging configurations for both console and file outputs.
- Richly formatted logs with tracebacks for easier debugging.
- Verbosity controls and custom markers for advanced filtering.
- Integrates with existing Python logging systems.

## Usage

### Basic Logging Setup

```python
from lifecyclelogging.logging import Logging

# Create a logger instance
logger = Logging(to_console=True, log_file_name="example_log")

# Log a statement
logger.logged_statement("This is an informational log.", log_level="info")
```

### Advanced Configuration

LifecycleLogging allows flexible configuration, including verbosity, custom markers, and more:

```python
logger.logged_statement(
    msg="This is a debug message.",
    verbosity=2,
    log_level="debug",
    active_marker="MY_MARKER"
)
```

### Integration with Gunicorn

LifecycleLogging detects and inherits Gunicorn log handlers automatically, ensuring seamless integration with web applications.

## Development

To contribute to LifecycleLogging:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/lifecyclelogging.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python -m unittest discover
   ```

## Documentation

The full documentation is available [here](docs/_build/html/index.html).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Happy Logging!**
