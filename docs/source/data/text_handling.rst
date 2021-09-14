.. _text_handling:

**Text**
========

Arjuna's :py:class:`Text <arjuna.tpi.parser.text.Text>` class provides with various factory methods to easily create a Text file object to read content in various formats:
    * **file_content**: Returns content as string.
    * **file_lines**: Returns :py:class:`TextFileAsLines <arjuna.tpi.parser.text.TextFileAsLines>` object to read file line by line.
    * **delimited_file**: Returns :py:class:`DelimTextFileWithLineAsMap <arjuna.tpi.parser.text.DelimTextFileWithLineAsMap>` or :py:class:`DelimTextFileWithLineAsSeq <arjuna.tpi.parser.text.DelimTextFileWithLineAsSeq>` object to read file line by line, parsed based on delimiter.

Following sections show the usage.

**Reading Text File** in One Go
-------------------------------

Reading complete content of a text file is pretty simple:

.. code-block:: python

    content = Text.file_content('/some/file/path/abc.text')

Reading Text File **Line by Line**
----------------------------------

Quite often you deal with reading of a text file line by line rather than as a text blob:

.. code-block:: python

    file = Text.file_lines('/some/file/path/abc.text')
    for line in file: # line is a Python **str** object.
        # Do something about the line
        print(line)
    file.close()

What Are **Delimited Text Files?**
----------------------------------

Delimited files are in widespread use in test automation. 

These files contain line-wise content where different parts of a line are separated by a delimiter. For example:

**Tab Delimited File**

.. code-block::

   Left	Right	Sum
   1	2	3
   4	5	8

**CSV File (Comma as the delimiter/separator)**

.. code-block::

   Left,Right,Sum
   1,2,3
   4,5,8

In the above examples, note that the first line is a header line which tells what each corresponding part of a line contains in subsequent lines.

The delimited files can also be created without the header line. For example:


.. code-block::

   1	2	3
   4	5	8

Although the above is not suggested, however at times you consume files from an external source as such and do not have much of an option.

Arjuna provides features to handle all of the above situations.


**Reading Delimited Text Files**
--------------------------------

Reading Delimited Text File with Header
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider the following tab-delimited file (let's name it abc.txt):

.. code-block::

   Left	Right	Sum
   1	2	3
   4	5	8

To read the above file, you can use the following Python code:

.. code-block:: python

    file = Text.delimited_file('/some/file/path/abc.text')
    for line in file: # line is a Python **dict** object e.g. {'Left' : '1', 'Right': 2, 'Sum' : 3}
        # Do something about the line
        print(line)
    file.close()

Tab is the default delimiter. If any other delimiter is used, then it needs to be specified by passing the **delimiter** argument.

For example, consider the following CSV file (let's call it abc.csv):

.. code-block::

   Left,Right,Sum
   1,2,3
   4,5,8

To read the above file, you can use the following Python code:

.. code-block:: python

    file = Text.delimited_file('/some/file/path/abc.text', delimiter=',')
    for line in file: # line is a Python **dict** object e.g. {'Left' : '1', 'Right': 2, 'Sum' : 3}
        # Do something about the line
        print(line)
    file.close()

Reading Delimited Text File WITHOUT Header
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the input file is without header line, you need to specify the same by passing **header_line_present** as False. The line is returned as a Python tuple object in this case instead of a dictionary object.

Consider the following tab-delimited file  without header line (let's name it abc.txt):

.. code-block::

   1	2	3
   4	5	8

To read the above file, you can use the following Python code:

.. code-block:: python

    file = Text.delimited_file('/some/file/path/abc.text', header_line_present=False)
    for line in file: # line is a Python **tuple** object e.g. (1,2,3)
        # Do something about the line
        print(line)
    file.close()
