.. _resources:

**Handling Test Resources**
===========================

What are Test Resources?
------------------------

More often than not, a test needs one or more resources. It could be a launched browser, an application in a certain state, a database handle and so on.

Such resources at times need to be shared across tests.

In Arjuna you can create resources at various levels and associate them with tests. The Arjuna markup for resources wraps pytest's corresponding test fixtures.


Resource Levels - **@for_group**, **@for_module**, **@for_test**
----------------------------------------------------------------

A resource is defined as a python function (a generator with a single yield to be precise) in Arjuna:

    .. code-block:: python

        def db(request):

            db_handle = create_db_handle()

            yield db_handle

            db_handle.quit()

In the above dummy resource code:
* There are three logical parts of a resource creator function.
* In first part you create the resource.
* In second part you yield it.
* In third part you clean up the resource.

To tell Arjuna, that it is a resource function, you need to decorate it with resource decorators. There are three of them available:
* **@for_group**: Create a resource at group level, once across all tests in the group.
* **@for_module**: Create a resource at module level, once across all tests in a module.
* **@for_test**: Create a resource for every test.

Following is an example using **@for_test**:
    .. code-block:: python

        @for_test
        def db(request):

            db_handle = create_db_handle()

            yield db_handle

            db_handle.quit()


**Module-Specific** Resources 
-----------------------------

You can place the resource functions in a test module python file. 

In such a case, these can be used only by the tests present in that module.

**Cross-Module** Shared Resources
---------------------------------

You might want to make resource functions available across your project.

To enable this, Arjuna tries to automatically import such resource creators with the following import (assume `testproj` as the project name):

    .. code-block:: python

        from testproj.lib.resource import *

To make use of this feature, you can choose to do one of the following depending on your requirements:

* If you have used `create-project` command of Arjuna CLI, you will observe that the command creates **<Project Root Directory>/lib/resource.py** module. You can add all resource creators here. They will be automnatically made available for your tests across the test modules in the project.
* For more complex project needs, where the resource creators grow in number, you can convert **resource.py** to a **resource package**. An example of this can be found in the `Arjex project on GitHub <https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex>`_.

**Data-Driven** Test Resources
------------------------------

You can data-drive a test resource as well just like you data-drive a test.

    .. code-block:: python

        @for_test(drive_with=<ds>)
        def db(request):
            print(request.data)

The resource creator function gets as many times as there are records in the data source.

Within the resource, you can act on data to create a custom resource.

The data can be acces from request object as **request.data** as a **DataRecord** object.

**Associating a Resource with a Test**
--------------------------------------

To associate a test resource with a test, pass its name as an argument:


    .. code-block:: python

        @test:
        def check_some_sql(request, db):
            ## Now you can act on what db resource yields. E.g.
            db.execute(some_sql)


Note that if the resource has been created at a higher level already (group/module level), it will not be created again.


Setting a **Resource as a Default**
-----------------------------------

You might-want to auto-create a resource i.e. make it a default at a certain level. When this is done, you don't need to pass the resource creator name as an argument to a test function.

Depending upon whether you have put the resource creator in a test module python file or in project library, these default resources are available to in a given module or across the test project.

To make a resource a default, use the **default** keyword argument:

    .. code-block:: python

    .. code-block:: python

        @for_group(default=True)
        def db(request):
            db_handle = create_db_handle()

            yield db_handle

            db_handle.quit()


