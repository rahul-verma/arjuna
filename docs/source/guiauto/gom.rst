.. _element:

Advanced Gui Abstraction
========================

Concept of Gui in Arjuna
------------------------

Graphical User Interfaces are represented using the `Gui` class in Arjuna. It provides all methods to interact with the Gui as well for creation of objects for its visual elements.

Arjuna has three types of `Gui`'s, namely `GuiApp`, `GuiPage` and `GuiSection` and any children thereof. 

Note that `GuiWidget` and `GuiDialog` are aliases for `GuiSection`currently, but this behavior could change in future.

The GuiApp Class
^^^^^^^^^^^^^^^^

In addition to directly creating an object of App, you can also inherit from it and extend it.

For example:

.. code-block:: python

   class WordPress(GuiApp):
   
    def __init__(self):
        url = C("wp.login.url")
        super().__init__(base_url=url)

Within the class' methods, you can now access its methods directly:

.. code-block:: python

   self.gns.abc # Element for abc label in GNS
   self.launch()

The GuiPage Class
^^^^^^^^^^^^^^^^^

You can implement a GuiPage by inheriting from `GuiPage` class:

.. code-block:: python

   class Home(GuiPage):
   
    def __init__(self, source_gui):
        url = C("wp.login.url")
        super().__init__(source_gui=source_gui)

A `GuiPage` must be provided with a `source_gui` i.e. the `Gui` from where the page is being created.

The GuiSection Class
^^^^^^^^^^^^^^^^^^^^

You can implement a GuiSection by inheriting from `GuiSection` class:

.. code-block:: python

   class LeftNav(GuiSection):
   
    def __init__(self, page):
        url = C("wp.login.url")
        super().__init__(page=page)

A `GuiSection` must be provided with a `page` i.e. the `GuiPage` for which the section is being created.

Gui Abstraction Models
----------------------

App Model using App class
^^^^^^^^^^^^^^^^^^^^^^^^^

You can implement a class as a `GuiApp` by using inheritance. This is the suggested way of implenting a web application abstraction in Arjuna. 

This is the simplest way to get started with an equivalent of GuiPage Object Model (POM), GuiPage Factories, Loadable Component, all clubbed into one concept. We represent the complete appplication as a single class which is attached to a a single GNS file for externalization. It should work well for small apps or where you are automating only a small sub-set of the application. 

App-Page Model using GuiApp and GuiPage Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For professional test automation, where you automate multiple use cases across different pages/screens, a simple App Model will not suffice. In the simple App Model, the GNS file will be cluttered with labels from multiple pages and the `GuiApp` class will have so many methods that it will impact code mainteance and understandability.

One step forward from Arjuna's App Model is the App-Page Model:
    #. You  implement the web application as a child of `GuiApp`class.
    #. We implemented each web page of interest as a child of `GuiPage` class.
    #. The `GuiPage` classes have methods to move from one page to another.

App-Page-Section Model using GuiApp, GuiPage and GuiSection Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider the following:
    1. Typcally, the web applications follow a set of a templates for different pages. Such templates have some repetitive sections across multiple pages. Examples: Left navigation bars, Top Menus, Sidebars etc.
    2. Some application pages might be two complex to be represented as a single page.
    3. Some similar HTML components like tables etc. are resued across multiple pages as a part of their contents.

Unless you address the above in the way you implement the Gui abstraction, the code will not clearly represent the Gui. Also, even if externalized, this could result in repeated identifiers across different GNS files.

One step forward from Arjuna's App-GuiPage Model is the App-GuiPage-GuiSection Model:
    1. Implement the web application as a child of `GuiApp`class.
    2. Implement each web page of interest as a child of `GuiPage` class.
    3. GuiPages inherit from different template base pages to represent common structures.
    4. Reusables page portions are implemented as `GuiSection`s and a correct composition relationship is established between a `GuiPage` and its `GuiSection`s using OOP.
    5. In short, Apps have pages and a page can have sections.

Arjuna's Gui Loading Model
--------------------------

All `Gui`s follow the `Gui Loading Mechanism` in Arjuna. For a `GuiApp`, loading logic is triggered when it is launched (`launch` method called). For `GuiPage` and `GuiSection` it takes place as a part of initialization (`super().__init__()` call.)

We can hook into the mechanism by implementing one or more of the three hooks made available by Arjuna to all `Gui`s. We don't need to do anything special to the `Gui` classes to make it happen. It is available by default. On the other end, if we don't want to use it, we don't need to do anything at all because all the hook methods are optional.

It draws inspiration from Selenium Java's implementation of Loadable Component but it is Arjuna's custom implementation using its own conditions and wait mechanism.

    1. Gui's `prepare` method is called with any `*args` and `**kwargs` provided in the `__init__` implementation of a child `Gui`. This is the method which you use for externalization of Gui definitions.
    2. Root Element is polled for, if defined, until `ArjunaOption.GUIAUTO_MAX_WAIT` number of seconds. In case of exception, loading stops here and `GuiNotLoadedError` is raised.
    3. Anchor Element is polled for, if defined, until `ArjunaOption.GUIAUTO_MAX_WAIT` number of seconds. In case of exception, loading stops here and `GuiNotLoadedError` is raised.
    4. `validate_readiness` method is called. If it does not raise any exception, then the loading mechanism stops here.
    5. If in **step 4**, an exception of type `arjuna.tpi.exceptions.WaitableError` (or its sub-type) is raised, then the next steps as mentioned in **Step 6 and 7** are performed, else `GuiNotLoadedError` exception is raised.
    6. Gui's `reach_until` method is called. If any exception is raised by it, then `GuiNotLoadedError` exception is raised, else **step 7** is executed.
    7. This time `validate_readiness` is called, but not directly. It is tied to the `GuiReady` condition which is polling wait-based caller. If `validate_readiness` raises an exception of type `arjuna.tpi.exceptions.WaitableError` (or its sub-type), `GuiReady` condition keeps calling it until `ArjunaOption.GUIAUTO_MAX_WAIT` number of seconds are passed in `Gui`'s configuration. If successful, during the wait time, then Gui is considered loaded, else `GuiNotLoadedError` exception is raised.
