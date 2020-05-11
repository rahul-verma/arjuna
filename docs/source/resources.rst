.. _resources:

What are Test Resources?
========================

More often than not, a test needs one or more resources. It could be a launched browser, an application in a certain state, a database handle and so on.

Such resources at times need to be shared across tests.

In Arjuna you can create resources at various levels and associate them with tests. The Arjuna markup for resources wraps pytest's corresponding test fixtures.


Resource Levels - **@for_group**, **@for_module**, **@for_test**
================================================================

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


Module Specific and Cross-Module Shared Resources
=================================================

