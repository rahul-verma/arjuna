### Gui and Its Loading Model in Arjuna

Arjuna has three types of `Gui`'s, namely `App`, `Page` and `Widget` and any children thereof.

All `Gui`s follow the `Gui Loading Mechanism` in Arjuna. For an `App` loading logic is triggered when it is launched (`launch` method called). For `Page` and `Widget` it takes place as a part of initialization (`super().__init__()` call.)

We can hook into the mechanism by implementing one or more of the three hooks made available by Arjuna to all `Gui`s. We don't need to do anything special to the `Gui` classes to make it happen. It is available by default. On the other end, if we don't want to use it, we don't need to do anything at all because all the hook methods are optional.

It draws inspiration from Selenium Java's implementation of Loadable Component but it is Arjuna's custom implementation using its own conditions and wait mechanism.

1. Gui's `prepare` method is called with any `*args` and `**kwargs` provided in the `__init__` implementation of a child `Gui`. This is the method which you use for externalization of Gui definitions.
2. Root Element is polled for, if defined, until `ArjunaOption.GUI_MAX_WAIT` number of seconds. In case of exception, loading stops here and `GuiNotLoadedError` is raised.
3. Anchor Element is polled for, if defined, until `ArjunaOption.GUI_MAX_WAIT` number of seconds. In case of exception, loading stops here and `GuiNotLoadedError` is raised.
4. `validate_readiness` method is called. If it does not raise any exception, then the loading mechanism stops here.
5. If in **step 4**, an exception of type `arjuna.core.exceptions.WaitableError` (or its sub-type) is raised, then the next steps as mentioned in **Step 6 and 7** are performed, else `GuiNotLoadedError` exception is raised.
6. Gui's `reach_until` method is called. If any exception is raised by it, then `GuiNotLoadedError` exception is raised, else **step 7** is executed.
7. This time `validate_readiness` is called, but not directly. It is tied to the `GuiReady` condition which is polling wait-based caller. If `validate_readiness` raises an exception of type `arjuna.core.exceptions.WaitableError` (or its sub-type), `GuiReady` condition keeps calling it until `ArjunaOption.GUI_MAX_WAIT` number of seconds are passed in `Gui`'s configuration. If successful, during the wait time, then Gui is considered loaded, else `GuiNotLoadedError` exception is raised.
