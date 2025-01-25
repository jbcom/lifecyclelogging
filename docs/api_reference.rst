================================
API Reference
================================

Logging Class
-------------

.. py:class:: lifecyclelogging.Logging

   Main class for managing application lifecycle logs.

   .. py:method:: __init__(to_console: bool = False, to_file: bool = True, ...)

      Initialize the Logging class.

   .. py:method:: logged_statement(msg: str, log_level: LogLevel = "debug", ...)

      Log a statement with optional data and verbosity controls.
