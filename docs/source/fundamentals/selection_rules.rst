.. _selection_rules:


**Test Selection Rules**
========================

Purpose
-------

Arjuna provides an advanced approach to test selection using its selection rule grammar.

The rules can be specified in the command line as well in Test Group definitions.

The rules are executed on the following:

* Built-in Test Attributes
* Built-in Tag Continers
* User-defined Properties

**Inclusion** vs **Exclusion** Rules
------------------------------------

The rules are categorized based on their inclusion effect:

**Inclusion rules** / **irule**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * If the specified rule matches, it leads to inclusion of a test function, or next level of checks (see next section).
    * Specified as **ir**

**Exclusion rules** / **erule**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * If the specified rule matches, it leads to exclusion of a test function.
    * Specified as **er**

Any number of these rules can be specified in CLI or test group definition.

**Rules Grammar**
-----------------

.. _boolean_pattern_rule:

**Boolean Pattern** Rule
^^^^^^^^^^^^^^^^^^^^^^^^

Simple Pattern for Boolean test attributes.

.. code-block:: text

    unstable
    not unstable

.. _iterable_pattern_rule:

**Iterable Pattern** Rule
^^^^^^^^^^^^^^^^^^^^^^^^^

Simple Pattern for presence/absence of strings in iterables.

.. code-block:: text

    with tags a,b
    withall tags a,b
    without tags a,b

* **with** keyword means an iterable that contains **ANY** of the provided names.
* **withall** keyword means an iterable that contains **ALL** of the provided names.
* **with** keyword means an iterable that **DOESNOT** contain **ANY** of the provided names.

You can use singular version as well - **tag/bug/env** for built-in containers.

.. _test_attr_rule:

**Test Attribute Pattern** Rule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pattern for executing a condition on an attribute value. This is the most advanced of all the patterns.

.. code-block:: text

    author is Rahul

It follows the structure:

.. code-block:: text

    attr operator value


When this rule is executed, it extracts the value of mentioned attribute for the test object and then compares it with the value using the operator defined.

Following is the list of all operators:

* **is**/**eq**/**=**: Is Equal
* **not**/**!=**/**ne**: Not Equal
* **matches**/**~=**: Matches (case insensitive)
* **!~=**: Does not match (case insensitive)
* ***=** Partial Match  (case insensitive)
* **!*=** No Partial Match (case insensitive)
* **lt**/**<**: Less Than
* **le**/**<=**: Lesser or Equal
* **gt**/**>**: Greater Than
* **ge**/**>=**: Greater or Equal

**Rule applicability**:

* Strings allow all operators.
* Numbers don't allow matching related operators.
* Booleans allow only equal/no equal operators. Better to use Boolen Pattern.
* Operators can be contextual. For example, for priority, priority 1 is higher than priority 2. Arjuna considers this in rule evaluation rather than treating it as just another integer.

.. _cli_group_customrules:

**Using Custom Test Selection Rules**
-------------------------------------

Arjuna defines an advanced grammar for selection of tests with its :ref:`selection_rules` (the linked page describes the rules grammar in detail.)

You can supply one or more selection rules in command line or write them in a group definition.

**Command-Line**
^^^^^^^^^^^^^^^^

In CLI, you can provide the following switches to provide rules:
    * **--irule**
    * **--erule**

Any number of the above switches can be provided. Following are some examples:

:ref:`boolean_pattern_rule` Example

    .. code-block:: text

        --irule unstable --irule "not reviewed"


:ref:`iterable_pattern_rule` Example

    .. code-block:: text

        --irule "with tags a,b" --irule "without tags x,y"


:ref:`test_attr_rule` Example

    .. code-block:: text

        --irule "author is Rahul" --irule "priority < 3"


Group Definition in **groups.yaml**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also add rules to the group definition in **groups.yaml**. 

Any number of such rules can be added.

Following are some examples where **sample_group** is the group name.

:ref:`boolean_pattern_rule` Example

    .. code-block:: yaml

        sample_group:
            irule:
                - "unstable"
                - "not reviewed"


:ref:`iterable_pattern_rule` Example

    .. code-block:: yaml

        sample_group:
            irule:
                - "with tags slow"
                - "without tags x,y"


:ref:`test_attr_rule` Example

    .. code-block:: yaml

        sample_group:
            irule:
                - "author is Rahul"
                - "priority < 3"

.. _shortcut_testselect:

**Shortcut Rules** for **Test Package, Module and Function Names**
------------------------------------------------------------------

A very common use case for test selection is based on packahe, module and/or function names.

Given the common usage of these in test automation world, Arjuna provides shortcut rules for these.

These can be provided using Command Line (refer :ref:`cli_rules`) as well as in Group Definitions (refer :ref:`test_group`).

**ipack**: Include Package
^^^^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to partial match for **package** test attribute: **package *= pkg_name_or_pattern**

**epack**: Exclude Package
^^^^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to unsuccessful partial match for **package** test attribute:  **package !*= pkg_name_or_pattern**

**imod**: Include Module
^^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to partial match for **module** test attribute:  **module *= module_name_or_pattern**

**emod**: Exclude Module
^^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to unsuccessful partial match for **module** test attribute:  **module !*= module_name_or_pattern**

**itest**: Include Test
^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to partial match for **name** test attribute:  **name *= function_name_or_pattern**

**etest**: Exclude Test
^^^^^^^^^^^^^^^^^^^^^^^

    * Internally translates to unsuccessful partial match for **name** test attribute:  **name !*= function_name_or_pattern**


Rule **Evaluation Sequence**
----------------------------

Arjuna follows a specific order in evaluating rules:

Rules are segregated as package, module and test rules (inclusion/exclusion).

Following is the test selection process as per Arjuna rules:

    #. Package check: Specified using ipack/epack or irule/erule with "package operator operand" grammar.
        - if package for a test meets an exclusion rule, it is excluded.
        - if no inclusion rule is specified, it is included for module validation.
        - if an inclusion rule is met, it is selected for module validation.
        - if no inclusion rule is met, it is excluded.
    #. Module check: Specified using imod/emod or irule/erule with "module operator operand" grammar.
        - if module for a test meets an exclusion rule, it is excluded.
        - if no inclusion rule is specified, it is included for test validation.
        - if an inclusion rule is met, it is selected for test validation.
        - if no inclusion rule is met, it is excluded.
    #. Test check: Specified using itest/etest or irule/erule with any rule grammar except "package operator operand" and "module operator operand".
        - if a test meets an exclusion rule, it is excluded.
        - if no inclusion rule is specified, it is included in test group run.
        - if an inclusion rule is met, it is included in test group run.
        - if no inclusion rule is met, it is excluded from test group run.

