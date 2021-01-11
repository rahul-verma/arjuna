.. _test_spaces:

**Data Spaces - Shareable Data Objects for Tests**
==================================================

**Need for Spaces in Test Automation**
--------------------------------------

Test resources are in general a great way for setting up pre-reqiusities and providing required resources to tests.

However, there are circumstances where you need to create and share data among tests. For example:

    * You want to setup a workflow (let's say 4 tests representing CRUD operations on object) where data setup by one test is then utlilized by the subsequent tests.
    * You want to maintain a data structure that contains consumable data.

**Types** of Spaces
-------------------

The space object is accesed using the **request** object that is passed to every test resource function as well as test function in Arjuna.

There are three types of test spaces that are provided to you:

**Group Space**
^^^^^^^^^^^^^^^

Within a **@for_group** test resource function, the following Python code refers to Group space:

.. code-block:: python

    # Implicitly
    request.space

    # Explicitly
    request.group.space

In other test resource functions or test functions, it must be explictly accessed:

.. code-block:: python

    # Explicitly
    request.group.space

**Module Space**
^^^^^^^^^^^^^^^^

Within a **@for_module** test resource function, the following Python code refers to Module space:

.. code-block:: python

    # Implicitly
    request.space

    # Explicitly
    request.module.space

In other test resource functions or test functions, it must be explictly accessed:

.. code-block:: python

    # Explicitly
    request.module.space

.. note::

    Module space is not accessible from a group resource function as it is at a lower level than group.

**Test Space**
^^^^^^^^^^^^^^

Within a **@for_test** test resource function or a test function, the following Python code refers to Test space:

.. code-block:: python

    request.space

.. note::

    Test space is not accessible anywhere else as it is the lowest space level.

**Defining and Utilizing Objects in Spaces**
--------------------------------------------

Declaring and accessing an object in any space is done as if you are dealing with a defined attribute of an object:

.. code-block:: python

    # Defining
    request.space.obj_name = some_value

    # Retrieving
    request.space.obj_name

    # Re-Assignment
    request.space.obj_name = new_obj

    # Modification (assume a dictionary)
    request.space.obj_name[2] = 4
    del request.space.obj_name[5]

**Test Space**
^^^^^^^^^^^^^^

This is the simplest to understand space and you will mostly utilize it to create objects in **@for_test** test resource functions which can then be used by test functions.

**Definition**

.. code-block:: python

    @for_test
    def tres(request):
        request.space.immutable = "testing"
        request.space.mutable = {1:2, 3:4}
        yield

**Access in Test Function**

.. code-block:: python

    @test
    def check_test_space(request, tres):
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4

**Access in @for_test Resource Function**

.. code-block:: python

    @for_test
    def another_tres(request, tres):
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

**Test Space is NOT Shared Among Tests**

Test Space is unique to a test and is not shareable. 

The following works perfectly as you are modifying the object within a test:

.. code-block:: python

    @test
    def check_test_space_modify(request, tres):
        request.space.immutable = "changed"
        request.space.mutable[5] = 6
        assert request.space.immutable == "changed"
        assert request.space.mutable[5] == 6

However, if you expect these changes to reflect in next test(s) in the run sequence, it will not work. Each test gets its own copy of the objects in Test Space:

.. code-block:: python

    @test
    def check_test_space_test(request, tres):
        assert request.space.immutable == "changed" # Fails
        assert request.space.mutable[5] == 6 # Will Fail if above is commented.

**Modifying Space Objects in **Multiple Test Resources** for a Test**

When you use multiple test resource functions for a given test, then its space is defined by all definitions and modifications done by these resource functions.

.. code-block:: python

    @for_test
    def tres_multi_1(request):
        request.space.something = "test"
        yield

    @for_test
    def tres_multi_2(request):
        assert request.space.something == "test"
        request.space.something = "changed"
        yield

    @test
    def check_space_multi_res(request, tres_multi_1, tres_multi_2):
        assert request.space.something == "changed"

Same is true if you are using the resource functions as a chain:

.. code-block:: python

    @for_test
    def tres_chain_1(request):
        request.space.something = "test"
        yield

    @for_test
    def tres_chain_2(request, tres_chain_1):
        assert request.space.something == "test"
        request.space.something = "changed"
        yield

    @test
    def check_space_chain(request, tres_chain_2):
        assert request.space.something == "changed"

**Module Space**
^^^^^^^^^^^^^^^^

The workings of Module space are similar to those of test space.

**Definition**

.. code-block:: python

    @for_module
    def mres(request):
        request.space.immutable = "testing" # Can use request.module.space as well.
        request.space.mutable = {1:2, 3:4}
        yield

**Accessing Module Space in Test Function (Explicit)**

.. code-block:: python

    @test
    def check_mod_space(request, mres):
        assert request.module.space.immutable == "testing"
        assert request.module.space.mutable[3] == 4

**Cross-Space Lookup in Arjuna (Test -> Module)**

If the named object that you want to find does not exist in Test Space, Arjuna automatically looks for it in Module Space and then in Group Space.

To use this lookup feature, rather than explicit lookup in a particular space, you should let Arjuna handle it.

This means instead of using the following in test function

.. code-block:: python

    request.module.space.x

if you use

.. code-block:: python

    request.space.x

it triggers the automatic lookup of Arjuna across spaces.

See the following section for this implicit lookup.

**Accessing Module Space in Test Function (Implicit)**

.. code-block:: python

    @test
    def check_mod_space(request, mres):
        # Looks in Test Space and then in Module Space.
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4

The above code works as Arjuna after not finding these objects in Test Space will automatically look for them in Module Space.

**Access in @for_module and @for_test Resource Functions**

The Module Space can be accessed in other module level as well as test resource functions:

.. code-block:: python

    @for_module
    def another_mres(request, mres):
        # Directly looks in Module Space
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

    @for_test
    def tres(request, mres):
        # Looks in Test Space and then in Module Space.
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

**Module Space is Shared Among Tests in SAME Module**

Unlike the Test Space, Module Space is shared among tests in a module.

It means modifications done by one test are seen by another:

.. code-block:: python

    @test
    def check_mod_space_modify(request, mres):
        request.module.space.immutable = "changed"
        request.module.space.mutable[5] = 6
        assert request.space.immutable == "changed"
        assert request.space.mutable[5] == 6

    # Test in same module, executed subsequently
    @test
    def check_mod_space_test(request, mres):
        assert request.space.immutable == "changed"
        assert request.space.mutable[5] == 6

**Creating and Sharing Data From Within Tests in a Module**

As the Module Space is shared among tests, you can create new objects in this space in a test function as well. These can then be accessed and/or modified in subsequent tests in the module.

In the following code **created_id** is defined in first test function and then accessed in the subsequent ones.

.. code-block:: python

    @test
    def check_crud_add(request):
        # Some object addition code followed by
        request.module.space.created_id = "abc123"

    @test
    def check_crud_edit(request):
        cid = request.space.created_id
        # Code to edit object for this id
        assert cid == "abc123"

    @test
    def check_crud_delete(request):
        cid = request.space.created_id
        # Code to delete object for this id
        assert cid == "abc123"


**Group Space**
^^^^^^^^^^^^^^^

The workings of Group space are similar to those of module space.

**Definition**

.. code-block:: python

    @for_group
    def gres(request):
        request.space.immutable = "testing" # Can use request.group.space as well.
        request.space.mutable = {1:2, 3:4}
        yield

**Accessing Group Space in Test Function (Explicit)**

.. code-block:: python

    @test
    def check_group_space(request, gres):
        assert request.group.space.immutable == "testing"
        assert request.group.space.mutable[3] == 4

**Cross-Space Lookup** in Arjuna (Test -> Module -> Group)**

If the named object that you want to find does not exist in Test Space, Arjuna automatically looks for it in Module Space and then in Group Space.

To use this lookup feature, rather than explicit lookup in a particular space, you should let Arjuna handle it.

This means instead of using the following in test function

.. code-block:: python

    request.group.space.x

if you use

.. code-block:: python

    request.space.x

it triggers the automatic lookup of Arjuna across spaces.

See the following section for this implicit lookup.

**Accessing Group Space in Test Function (Implicit)**

.. code-block:: python

    @test
    def check_group_space(request, gres):
        # Looks in Test Space, then in Module Space and then in Group Space
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4

The above code works as Arjuna after not finding these objects in Test Space will automatically look for them in Group Space.

**Access in @for_group, @for_module and @for_test Resource Functions**

The Group Space can be accessed in all other resource functions:

.. code-block:: python

    @for_group
    def another_gres(request, gres):
        # Directly looks in Group Space
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

    @for_module
    def mres(request, mres):
        # Looks in Module Space and then in Group Space
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

    @for_test
    def tres(request, mres):
        # Looks in Test Space, then in Module Space and then in Group Space
        assert request.space.immutable == "testing"
        assert request.space.mutable[3] == 4
        yield

**Group Space is Shared Among Tests Across Modules**

Unlike the Test Space, Group Space is shared among tests.

Unlike the Module Space, Group Space is shared among tests in across modules.

It means modifications done by one test are seen by another:

.. code-block:: python

    @test
    def check_group_space_modify(request, mres):
        request.module.space.immutable = "changed"
        request.module.space.mutable[5] = 6
        assert request.space.immutable == "changed"
        assert request.space.mutable[5] == 6

    # Test in same or different module, executed subsequently
    @test
    def check_group_space_test(request, mres):
        assert request.space.immutable == "changed"
        assert request.space.mutable[5] == 6

**Creating and Sharing Data From Within Tests Across Modules**

As the Group Space is shared among tests across modules, you can create new objects in this space in a test function as well. These can then be accessed and/or modified in subsequent tests in any other module.

In the following code **created_id** is defined in first test function and then accessed in the subsequent ones.

.. code-block:: python

    @test
    def check_crud_add(request):
        # Some object addition code followed by
        request.group.space.created_id = "abc123"

    # Test in same or different module, executed subsequently
    @test
    def check_crud_edit(request):
        cid = request.space.created_id
        # Code to edit object for this id
        assert cid == "abc123"

    # Test in same or different module, executed subsequently
    @test
    def check_crud_delete(request):
        cid = request.space.created_id
        # Code to delete object for this id
        assert cid == "abc123"
