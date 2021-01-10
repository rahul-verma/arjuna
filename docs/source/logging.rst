.. _logging:


Introduction
------------

Arjuna's logging features as provided by :py:mod:`log <arjuna.tpi.log>` module, give you precise control over what is included in console display and log file.

For each test run, Arjuna creates a log file with the name **arjuna.log** in **<Test Project Directory>/report/<run report dir>/log** directory.

**Arjuna's Logging Functions** to Support Python Logging Levels
---------------------------------------------------------------

Arjuna provides individual logging functions to support the default Python logging levels:

    * DEBUG - :py:func:`log_debug <arjuna.tpi.log.log_debug>`
    * INFO - :py:func:`log_info <arjuna.tpi.log.log_info>`
    * WARNING - :py:func:`log_warning <arjuna.tpi.log.log_warning>`
    * ERROR - :py:func:`log_error <arjuna.tpi.log.log_error>`
    * FATAL - :py:func:`log_fatal <arjuna.tpi.log.log_fatal>`

The levels work just like Python logging levels. **FATAL** has the top priority and **DEBUG** has the least.

Controlling Which Log Messages Are Included on Console and in Log File
----------------------------------------------------------------------

When you set a log level, only the log messages that are of same or higher priority get logged.

For example, setting a log level to **WARNING** would mean:

    * Calls to **log_warning**, **log_error** and **log_fatal** will be entertained.
    * Calls to **log_info** and **log_debug** will be ignored.

**Default** Logging Levels
--------------------------

Default logging level for console is **INFO**.

Default logging level for log file (arjuna.log) is **DEBUG**.

Arjuna's **TRACE** Log Level
----------------------------

Arjuna adds an additional level of logging - **TRACE** - which is of lower priority than **DEBUG**.

This is parimarily added so that Arjuna's internal logging is kept to a minimum even when the logging is taking place at **DEBUG** level.

You can use it in your test project with a similar goal by using :py:func:`log_trace <arjuna.tpi.log.log_trace>` call.

**Overriding Logging Level Defaults**
-------------------------------------

You can change Arjuna's logging level defaults using the following commands in command line:

    * **-dl** / **--display-level**: Set level for console logging.
    * **-ll** / **--log-level**: Set level for file logging (arjuna.log)

**Contextual Logging**
----------------------

This is an advanced feature provided by Arjuna.

You can set one or more contexts (strings) to log messages.

    .. code-block:: python

        log_info("test context 2", contexts="test2")
        log_info("test context 4", contexts={"test3", "test4"})

A log message with a context(s) set for it does not get logged by default in Arjuna. It is only logged when **ArjunaOption.LOG_ALLOWED_CONTEXTS** has been accordingly set to include the context string. This can be done by any of the following means:

    * Passing **--ao LOG_ALLOWED_CONTEXTS <comma separated context strings>** to the command line.
    * Overrding LOG_ALLOWED_CONTEXTS in the reference configuration.

Note: Log messages without contexts set for them will work as usual and are not impacted by the **LOG_ALLOWED_CONTEXTS** option.


**Auto-Logging** using **@track** Decorator
-------------------------------------------

Many a times, you want to log messages at the beginning and end of a Python function/method call.

This is a primary use case and usually depends on test author's commitment to logging (and needs conscious efforts.)

Tracking **Methods, Functions, Properties**
-------------------------------------------

Arjuna's solves this by provding auto-logging using its :py:func:`@track <arjuna.tpi.tracker.track>` decorator. It will log:

    * Beginning of the call with provided arguments.
    * End of the call with return value (Long return values are truncated for brevity.)
    * Exceptions and exception trace if any exception is raised in calling the given function/method/property.

You can use **@track** with:
    * Functions
    * Bound Methods in a class
    * Class Methods in a class
    * Static Methods in a class
    * Properties in a class

Following are some samples:

    .. code-block:: python

        # Function
        @track
        def test1(self, a, *vargs, b=None, **kwargs):
            log_debug("in test1")

        class MethodTrack:

            # Bound Method
            @track
            def test1(self, a, *vargs, b=None, **kwargs):
                log_debug("in test1")

            # Class method
            @track
            @classmethod
            def cls_method_1(cls, a):
                log_debug("in cls_method")

            # Static Method
            @track
            @staticmethod
            def stat_method_1(a):
                log_debug("in stat_method")

            # Property getter
            @track
            @property
            def prop1(self):
                log_debug("prop1 getter")
                return self._p

            # Property setter. Note that just setting this will also decorate the getter.
            @track
            @prop1.setter
            def prop1(self, value):
                log_debug("prop1 setter")
                self._p = value

Tracking **All Methods** in a Class
-----------------------------------

If you want to track all methods in a class, you can decorate the class with **@track** rather than decorating all individual methods.

This will:

    * Track all
        * Bound Methods in a class
        * Class Methods in a class
        * Static Methods in a class
    * NOT track:
        * properties (They still need to be individually decorated.)

Following is a sample:

    .. code-block:: python

        @track
        class ClassTrack:

            def __init__(self, a, *vargs, b=None, **kwargs):
                log_debug("in __init__")

            def test1(self, a, *vargs, b=None, **kwargs):
                log_debug("in test1")

            @classmethod
            def cls_method(cls, a):
                log_debug("in cls_method")

            @staticmethod
            def stat_method(a):
                log_debug("in stat_method")


**Default Logging Level** for @track
------------------------------------

To control verbosity of logging, @track uses the following default logging levels:

    * **DEBUG** for all public methods.
    * **TRACE** for all protected (begin with "_"), private (begin with "__") and magic methods (the dunder methods begin and end with "__")

**Changing Logging Level** for @track
-------------------------------------

You can change the logging level for an object decorated with **@track** by providing the level as argument:

    .. code-block:: python

        @track("info")
        class ClassTrackInfo:
            pass

Note: This does not impact logging level for non-public methods.










