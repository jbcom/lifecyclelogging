================================
Getting Started
================================

Installation
-----------

You can install LifecycleLogging using pip:

.. code-block:: bash

   pip install lifecyclelogging

Quick Start
----------

Basic Usage
~~~~~~~~~~

Here's a simple example of using LifecycleLogging:

.. code-block:: python

   from lifecyclelogging import Logging

   # Initialize logger with console output
   logger = Logging(to_console=True)

   # Log messages at different levels
   logger.logged_statement("Starting application", log_level="info")
   logger.logged_statement("Processing data", log_level="debug")
   logger.logged_statement("Warning: high memory usage", log_level="warning")

File Logging
~~~~~~~~~~~

To log to a file instead of (or in addition to) the console:

.. code-block:: python

   # Initialize logger with file output
   logger = Logging(
       to_file=True,
       log_file_name="app.log"
   )

   # Messages will be written to app.log
   logger.logged_statement("This goes to the log file", log_level="info")

JSON Data Logging
~~~~~~~~~~~~~~~

LifecycleLogging can handle structured data:

.. code-block:: python

   data = {
       "user_id": 123,
       "action": "login",
       "timestamp": "2025-01-25T10:00:00Z"
   }

   logger.logged_statement(
       "User login",
       json_data=data,
       log_level="info"
   )

Log Markers
~~~~~~~~~~

You can group related log messages using markers:

.. code-block:: python

   logger = Logging(log_marker="user_activity")

   logger.logged_statement(
       "User profile updated",
       log_level="info"
   )

   # Access logs by marker
   user_logs = logger.logs["user_activity"]

Verbosity Control
~~~~~~~~~~~~~~~

Control log output verbosity:

.. code-block:: python

   logger.logged_statement(
       "Detailed debug info",
       verbose=True,
       verbosity=2,
       log_level="debug"
   )

Development Setup
---------------

For development:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/user/lifecyclelogging.git
   cd lifecyclelogging

   # Install development dependencies
   pip install -e ".[dev,test,docs]"

   # Run tests
   tox

   # Run specific checks
   tox -e lint  # Run linting
   tox -e type  # Run type checking