================================
Usage Guide
================================

Configuration
-----------

Logger Initialization
~~~~~~~~~~~~~~~~~~~

The LifecycleLogging package provides multiple configuration options:

.. code-block:: python

   from lifecyclelogging import Logging

   logger = Logging(
       to_console=True,        # Enable console output
       to_file=True,          # Enable file output
       logger_name="myapp",   # Custom logger name
       log_file_name="app.log", # Custom log file name
       log_marker="app"       # Default marker for logs
   )

Log Levels
---------

Available log levels from lowest to highest priority:

.. code-block:: python

   logger.logged_statement("Debug message", log_level="debug")
   logger.logged_statement("Info message", log_level="info")
   logger.logged_statement("Warning message", log_level="warning")
   logger.logged_statement("Error message", log_level="error")
   logger.logged_statement("Critical message", log_level="critical")

Structured Logging
----------------

JSON Data
~~~~~~~~

Log structured data along with messages:

.. code-block:: python

   logger.logged_statement(
       "API request",
       json_data={
           "method": "POST",
           "endpoint": "/api/v1/users",
           "status": 200
       },
       log_level="info"
   )

Labeled JSON Data
~~~~~~~~~~~~~~

Log multiple JSON objects with labels:

.. code-block:: python

   logger.logged_statement(
       "Data analysis",
       labeled_json_data={
           "input": {"rows": 1000, "columns": 5},
           "output": {"processed": 950, "errors": 50}
       },
       log_level="info"
   )

Advanced Features
--------------

Log Markers
~~~~~~~~~~

Group related logs using markers:

.. code-block:: python

   # Set marker during initialization
   logger = Logging(log_marker="database")

   # Or set marker for specific statements
   logger.logged_statement(
       "Query executed",
       log_marker="database",
       log_level="info"
   )

   # Access logs by marker
   database_logs = logger.logs["database"]

Verbosity Controls
~~~~~~~~~~~~~~~

Control output detail level:

.. code-block:: python

   # Basic verbosity
   logger.logged_statement(
       "Basic info",
       verbose=False,
       log_level="info"
   )

   # Detailed output
   logger.logged_statement(
       "Detailed info",
       verbose=True,
       verbosity=2,
       log_level="debug"
   )

Error Tracking
~~~~~~~~~~~

Track and access errors:

.. code-block:: python

   # Log an error
   logger.logged_statement(
       "Operation failed",
       log_level="error"
   )

   # Access error information
   last_error = logger.last_error
   last_error_message = logger.last_error_message
   all_errors = logger.errors

Environment Variables
------------------

Configuration via environment variables:

.. code-block:: bash

   # Set log level
   export LOG_LEVEL=DEBUG

   # Override console/file output
   export OVERRIDE_TO_CONSOLE=True
   export OVERRIDE_TO_FILE=True

   # Set custom log file name
   export LOG_FILE_NAME=custom.log

Best Practices
------------

1. **Log Level Selection**
   - Use "debug" for detailed troubleshooting
   - Use "info" for general operational events
   - Use "warning" for potentially harmful situations
   - Use "error" for error events that might still allow the application to continue
   - Use "critical" for critical errors that prevent program execution

2. **Structured Data**
   - Use json_data for single objects
   - Use labeled_json_data for multiple related objects
   - Keep data structures clean and readable

3. **Markers**
   - Use consistent naming conventions
   - Group related functionality
   - Consider hierarchical markers (e.g., "database.query", "database.connection")

4. **Performance**
   - Use appropriate verbosity levels
   - Consider log rotation for file outputs
   - Monitor log file sizes