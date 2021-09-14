.. _yaml_handling:

**YAML**
========

YAML is a popular format used in configurations. It is also the default format for Arjuna configuration and definition files.

Creating YAML Objects
---------------------

Arjuna's :py:class:`Json <arjuna.tpi.parser.yaml.Yaml>` class provides with various helper methods to easily create a YAML object from various sources:

    * **from_file**: Load YAML from a file.
    * **from_str**: Load YAML from a string.
    * **from_object**: Load YAML from a Python built-in data type object.

The loaded object is returned as one of the following:
    * :py:class:`YamlDict <arjuna.tpi.parser.yaml.YamlDict>`
    * :py:class:`YamlList <arjuna.tpi.parser.yaml.YamlList>`
    * If `allow_any` is set to True, then **from_file**, **from_str** and **from_object** calls return the same object as passed, if it is not a mapping or iterable.

**YamlDict** Object
-------------------

:py:class:`YamlDict <arjuna.tpi.parser.yaml.YamlDict>` encapsulates the YAML dictionary and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the YamlDict

**YamlList** Object
-------------------

:py:class:`YamlList <arjuna.tpi.parser.yaml.YamlList>` encapsulates the YAML list and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the JsonList


**==** Operator with **YamlDict** and **YamlList** Objects
----------------------------------------------------------

**==** operator is overridden for  **YamlDict** and **YamlList** objects.

YamlDict supports comparison with a YamlDict or Python dict.

YamlList supports comparision with a YamlList or Python list.

    .. code-block:: python

        yaml_dict_1 == yaml_dict_2
        yaml_dict_1 == py_dict

        yaml_list_1 == yaml_list_2
        yaml_list_1 == py_list

Using **!join** construct
-------------------------

Arjuna provides **!join** construct to easily construct strings by concatenating the provided list. For example:

    .. code-block:: YAML

        root: &BASE /path/to/root
        patha: !join [*BASE, a]
        pathb: !join [*BASE, b]

Once loaded this YAML is equivalent to the following Python dictionary:

    .. code-block:: python

        {
            'root': '/path/to/root', 
            'pathaa': '/path/to/roota', 
            'pathb': '/path/to/rootb'
        }

