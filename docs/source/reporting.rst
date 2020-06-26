.. _reporting:

HTML and Junit-Style XML Reporting
==================================

Arjuna currently supports two formats for reporting:

    * HTML: Arjuna wraps pytest-html reporting plugin for its HTML reports and adds its own JS/CSS extensions as well as more information controlled by Arjuna Options.
    * XML: Junit-style XMl report is generated for integration with CI applications like Jenkins.

Report Structure
----------------

For each run, Arjuna generates reports in a directory that is controlled by the RUN ID set for the run.

    - With defaults:
        * Default Run ID is **mrun**.
        * Arjuna appends current timestamp to the run id to generate the final run id.
        * This directory is created in **<Project Root>/report** directory.
        * Following sub-directories are created in it:
            * html: HTML report(s)
            * xml: XML Report(s)
            * log: Arjuna log.
            * screenshot: Screenshots taken in this run.
    - You can provide a custom run id e.g. "abc-beta" using CLI's **-r** / **--run-d** switches.
    - During development of scripts, you might want to update same reports. For this you can use CLI's **--update** switch. If provided, Arjuna does not append timestamp to run id for directory name, thereby overwriting previous report files.


Report File Names
-----------------

For run-project and run-selected Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The name of HTML report is **report.html** and for XML it is **report.xml**.

For run-session, run-stage and run-group Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The name of the report file is generated as:

    .. code-block:: text

        report-<session name>-<stage-name>-<group-name>.{html/xml}

Choosing Reporting Format
-------------------------

By default both report formats (XML and HTML) are generated.

You can control this by ArjunaOption.REPORT_FORMATS option in reference configuration.

You can also easily control this by CLI's **-o** / **--output-format** switch.

Reporting Protocols
-------------------

Additional contents in HTML reports are controlled using Arjuna's reporting protocols.

Screenshooter Protocol
^^^^^^^^^^^^^^^^^^^^^^

If the request object associated with a test resource or a test has a **screen_shooter** in its space, Arjuna takes a screenshot in case of failure and error situation and includes it in HTML report.

A **screenshooter** is any object that inherits and implements :py:class:`ScreenShooter <arjuna.tpi.protocol.screen_shooter.ScreenShooter>` base class.

Arjuna's **GuiApp** and **GuiPage** classes implement this and hence are screenshooters.

A suggested pattern to enable this feature is to do the following in a test resource function:

    .. code-block:: python

        request.space.screen_shooter = <app object or other screenshooter>

