.. _intro:

Emails in the Context of Test Automation
========================================

Some parts of your application might interact with an email server. An example is a password reset functionality.

Most commonly used functionality in test automation related to emails is the ability to read emails.

Solving this problem as a GUI automation problem has the usual glitches of GUI automation in terms of efforts of implementation as well as maintenance.

Arjuna currently provides Email reading and parsing capabilities using the IMAP protocol.

You might be testing an email server itself. This is currently not the focus of the implementation.