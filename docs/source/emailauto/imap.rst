.. _imap:

**Automating Email Reading**
============================

Arjuna provides you with library components for reading emails.

IMAP is used as the underlying protocol.

Following are the steps for a basic flow:
    * Create an instance of IMAP server.
    * Get an instance of a mailbox (for example, Inbox)
    * Read email(s) using the mailbox API.
    * Quit the email server.

Go through the following sections for these steps and specific use cases.

**Connecting to Email Server**
------------------------------

You can easily connect to an email server for the purpose of reading emails by providing basic connection details.

.. code-block:: python

    server = EmailServer.imap(
        host="host name or ip address", 
        port=345 # Provide correct port for SSL/non-SSL mode for your target server,
        user="some user account", 
        password="password", 
        use_ssl=True # Do you want to use IMAPS (SSL Mode) or IMAP (non-SSL mode)
    )

    # Once the activities are completed, quit the server
    server.quit()

**Default Configuration Settings** in Arjuna for Email Server
-------------------------------------------------------------

Arjuna has the following default settings for the following parameters:
    * **host**: localhost
    * **port**: 143 for non-SSL Mode and 993 for SSL-Mode.
    * **use_ssl**: True

You can make use of one or all of these defaults in your code:

.. code-block:: python

    server = EmailServer.imap(
        user="some user account", 
        password="password"
    )

    # Once the activities are completed, quit the server
    server.quit()


**Project-Level Default Configuration** for Email Server
--------------------------------------------------------

You can override Arjuna's default settings as well as configure user account details in your test project.

As project level defaults are overridable in a reference configuration or CLI options, you can try these options as well for more dynamic requirements.

Following are the Arjuna options to be used in **project.yaml** file:

.. code-block:: yaml

    arjuna_options:
        emailauto.imap.host: some_host_or_ip_address
        emailauto.imap.port: port_as_integer
        emailauto.imap.usessl: TrueOrFalse
        emailauto.user: some_user_email
        emailauto.password: password

You can connect to the server using all these settings with a simple call:

.. code-block:: python

    server = EmailServer.imap()

    # Once the activities are completed, quit the server
    server.quit()


**Accessing a Mailbox** from Server
-----------------------------------

To get access to mailbox, use the get_mailbox call. By default, Inbox is returned.

.. code-block:: python

    mailbox = server.get_mailbox() # For Inbox
    mailbox = server.get_mailbox("mailbox_name") # For any other mailbox

**Reading Latest Emails**
-------------------------

Using the mailbox object, you can read emails using the **emails** method.

.. code-block:: python

    emails = mailbox.emails()

By default latest 5 emails are returned.

You can change the count using the **max** parameters:

.. code-block:: python

    emails = mailbox.emails(max=20, latest=False)

You can also use **latest** call for more readable code:

.. code-block:: python

    emails = mailbox.latest()
    emails = mailbox.latest(max=20)

**Reading Oldest Emails**
-------------------------

At times, you might want to read the oldest emails.

You can do this by setting **latest** parameter to False.

.. code-block:: python
    
    emails = mailbox.emails(latest=False) # Oldest 5 emails
    emails = mailbox.emails(max=20, latest=False) # Oldest 20 emails

**Reading Email at an ordinal**
-------------------------------

Although rare in usage, but if you want to read an email at a paticular ordinal position (human counting), you can do that as well:

Remember that ordinal numbers are from oldest to newest.

You can do this by setting **latest** parameter to False.

.. code-block:: python
    
    email = mailbox.email_at(7) # 7th oldest email


**Filtering Emails**
--------------------

You can further filter latest/oldest emails using one or more of the provided filters in **emails** as well as **latest** methods.

If you use more than one filter, all of them should be true for an email to be included in results.


**Filtering** Emails by **Sender**
----------------------------------

You can filter emails by sender. Case insensitive and partial match is used by Arjuna.

.. code-block:: python
    
    mailbox.latest(sender="email or partial text")
    mailbox.emails(sender="email or partial text")

**Filtering** Emails by **Subject**
-----------------------------------

You can filter emails by subject. Case insensitive and partial match is used by Arjuna.

.. code-block:: python
    
    mailbox.latest(subject="full or partial subject line")
    mailbox.emails(subject="full or partial subject line")

**Filtering** Emails by **Content**
-----------------------------------

You can filter emails by content. Case insensitive and partial match is used by Arjuna.

.. code-block:: python
    
    mailbox.latest(content="partial content")
    mailbox.emails(content="partial content")

**Reading New Emails - The Challenges**
---------------------------------------

This is the trickiest part in automation of reading emails.

A mailbox is a dynamic entity.
    * It can receive emails which are not triggered by activity in a test.
    * There might be a time delay in receipt of email in mailbox from the time an email-sending activity is triggered by a test.

For the above reasons, you need two things:
    * A state-aware code to differentiate existing and new emails.
    * Polling mechanism to wait for new emails to arrive.

**Reading New Emails - One Time**
---------------------------------

Consider the following simple scenario:
    * Connect to mail server
    * Connect to mailbox
    * Trigger email sending actvitiy
    * Read new emails (one time)
    * Process the emails as per your requirement
    * Quit the server

For such one time activity and reading of new emails, Arjuna automatically handles the state for you.

.. code-block:: python

    # Stage 1 - Connect to mailbox
    server = EmailServer.imap() # Connect to server
    mailbox = server.get_mailbox() # Get access to Inbox

    # Stage 2 - Trigger one or more events for sending email(s)

    # Stage 3 - Read emails
    emails = mailbox.new_emails()

    # Stage 4 - Process the emails
    
    # Stage 5 - Quit the server
    server.quit()

In the above code:
    * At end of stage 1, Arjuna automatically saves the current mailbox state.
    * At stage 3, Arjuna triggers a dynamic wait for new emails and returns only new emails.

**Reading New Emails - Multiple Times**
---------------------------------------

Consider the following scenario:
    * Connect to mail server
    * Connect to mailbox
    * Trigger email sending actvitiy
    * Read new emails (one time)
    * Trigger email sending actvitiy
    * Read new emails (one time)
    * Trigger email sending actvitiy
    * Read new emails (one time)
    * ...
    * Quit the server

For this kind of successive new email reading activity, you will need to ask Arjuna to save state explicitly using the **save_state** call.

.. code-block:: python

    # Connect to mailbox
    server = EmailServer.imap() # Connect to server
    mailbox = server.get_mailbox() # Get access to Inbox
    mailbox.save_state() # Optional for first time. Included for completeness sake.

    # Trigger one or more events for sending email(s)

    # Read emails
    emails = mailbox.new_emails()

    # Process the emails

    mailbox.save_state()

    # Trigger one or more events for sending email(s)

    # Read emails
    emails = mailbox.new_emails()

    # Process the emails

    mailbox.save_state()

    # Trigger one or more events for sending email(s)

    # Read emails
    emails = mailbox.new_emails()

    # Process the emails

    mailbox.save_state()

    # And so on...
    
    # Stage 5 - Quit the server
    server.quit()

**Processing Emails**
---------------------

Once you have got emails from the server using any of the above mentioned approaches, you would want to read the content of such emails or extract certain parts of an email.

All of above mentioned email-fetching calls (apart from **email_at**) return an Arjuna **Emails** object.

The **Emails** object is like a Python list, so you can do the following operations:

.. code-block:: python

    emails.count() # Get Number of emails 
    len(emails) # Get Number of emails

    emails[index] # Get email at a particular index.

However, in practice, you would want to loop over this object and then process individual emails.

In each loop/iteration, you get Arjuna's **Email** object which is a very powerful abstraction to easily gt email meta-data and contents.

.. code-block:: python

    for email in emails:

        # Do something about a given email

**Inquire Email Meta-Data**
---------------------------

You can get various pieces of meta-data of an email using its properties and methods:

.. code-block:: python

    email.sender # content of From field
    email.recipient # content of To field 
    email.date # Received date
    email.subject # Subject line
    email.get_header("some-header-name") # Get data for any standard/custom header

**Get Email Contents**
----------------------

An email typically contains a chain of contents. Arjuna provides these contents as a list of Arjuna's **Text** and **Html** objects.

Attachments are not supported as of now.

.. code-block:: python

    content_list = email.contents

Depending on the type of content at a particular index, you can use the corresponding methods to process it further.

**Extracting Links from the Email**
-----------------------------------

As the most common scenario in email reading related automation is to extract links from the email, Arjuna's **Email** object provides built-in advanced methods for this use case.

Consider the following common scenario from Web GUI automation:
    * GUI Automation - In the test, you click a forgot password link and provide email address. 
    * Email Automation - You wait for the email to be got in the corresponding mailbox
    * Email Automation - You extract the password reset link from latest email.
    * GUI Automation - You go to the extracted link and finish password reset use case.

You can extract all links from the content chain of an email by using its **links** property:

.. code-block:: python

    email.links

You can get unique links (remove duplicates) from the content chain of an email by using its **unique_links** property:

.. code-block:: python

    email.unique_links

You can also get all the unqiue links by filtering based on a partial content of the link:

.. code-block:: python

    email.find_link(contains="somedomain") # Get first link based on its partial link text.
    email.find_links(contains="somedomain") # Get all links based on its partial link text.

























