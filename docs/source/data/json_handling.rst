.. _json_handling:

**JSON** (Javascript Object Notation)
=====================================

Json is a popular format used in RESTful services and configurations.

Creating **JSON Objects**
-------------------------

Arjuna's :py:class:`Json <arjuna.tpi.parser.json.Json>` class provides with various helper methods to easily create a Json object from various sources:

    * **from_file**: Load Json from a file.
    * **from_str**: Load Json from a string.
    * **from_map**: Load Json from a mapping type object.
    * **from_iter**: Load Json from an iterable.
    * **from_object**: Load Json from a Python built-in data type object.

The loaded object is returned as one of the following:
    * :py:class:`JsonDict <arjuna.tpi.parser.json.JsonDict>`
    * :py:class:`JsonList <arjuna.tpi.parser.json.JsonList>`
    * If `allow_any` is set to True, then **from_file**, **from_str** and **from_object** calls return the same object as passed, if it is not a mapping or iterable.

Json Class **Assertions**
-------------------------

Json class provides the following assertions:

    * **assert_list_type**: Validate that the object is a JsonList or Python list
    * **assert_dict_type**: Validate that the object is a JsonDict or Python dict

**Automatic Json Schema** Extraction
------------------------------------

Given a Json object, you can extract its schema automatically:

    .. code-block:: python

        Json.extract_schema(jsonobject_or_str)

This schema can be used for schema validation for another Json object.

**JsonDict** Object
-------------------

:py:class:`JsonDict <arjuna.tpi.parser.json.JsonDict>` encapsulates the Json dictionary and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the JsonDict
    * **schema**: The Json schema of this JsonDict (as a JsonSchema object)


**Finding Json elements** in a **JsonDict** Object
--------------------------------------------------

You can find Json elements in JsonDict by using a key name or by creating a more involved **JsonPath** query.

    * **find**: Find first match using a key or JsonPath
    * **findall** Find all matches using a JsonPath

**Matching Schema** of a **JsonDict** Object
--------------------------------------------

You can use a custom Json schema dictionary or a :py:class:`JsonSchema <arjuna.tpi.parser.json.JsonSchema>` object to validate schema of a **JsonDict** object.

    .. code-block:: python

        json_dict.matches_schema(schema)

It returns True/False depending on the match success.

**Asserting JsonDict** Object
-----------------------------

**JsonDict** object provides various assertions to validate its contents:

    * **assert_contents**: Validate arbitary key-value pairs in its root.
    * **assert_keys_present**: Validate arbitrary keys
    * **assert_match**: Assert if it matches another Python dict or JsonDict.
    * **assert_schema** Assert if it matches provided schema dict or JsonSchema.
    * **assert_match_schema** Assert if it has the same schema as that of the provided dict or JsonDict.


**JsonList** Object
-------------------

:py:class:`JsonList <arjuna.tpi.parser.json.JsonList>` encapsulates the Json list and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the JsonList


**==** Operator with **JsonDict** and **JsonList** Objects
----------------------------------------------------------

**==** operator is overridden for  **JsonDict** and **JsonList** objects.

JsonDict supports comparison with a JsonDict or Python dict.

JsonList supports comparision with a JsonList or Python list.

    .. code-block:: python

        json_dict_1 == json_dict_2
        json_dict_1 == py_dict

        json_list_1 == json_list_2
        json_list_1 == py_list

**Size Related Assertions** in **JsonDict** and **JsonList** Objects
--------------------------------------------------------------------

**JsonDict** and **JsonList** both extend the **IterableAsserterMixin** and hence provide the following size related assertions.

Note that size for JsonList means number of objects/elements in it and for JsonDict means number of keys in its root.

    * **assert_empty**: Validate that it is empty (size=0)
    * **assert_not_empty**: Validate size >= 1
    * **assert_size**: Validate size = provided size.
    * **assert_min_size**: Validate size >= provided size.
    * **assert_max_size**: Validate size <= provided size.
    * **assert_size_range**: Validate provided min size <= actual size <= provided max size

**Modifying JsonSchema** Object
-------------------------------

**JsonSchema** object is primarily targeted to be created using auto-extraction using **Json.extract_schema**.

You can currently make two modifications to the **JsonSchema** once created:

    * **mark_optional**: Mark arbitrary keys as optional in the root of the schema.
    * **allow_null**: Allow `null` value for the arbitrary keys.
