.. _locators_ext_axes:

**Arjuna Advanced Locators: Axes Locator**
==========================================

In DOM, if you are at a specific GuiWidget, then there are four basic directions of movement:
    * Up: Towards ancestors
    * Down: Towards descendants
    * Left: Towards preceding siblings
    * Right: Towards successding siblings

All the above directions of movements are supported in XPath.

Arjuna provides its **axes** locator to cater to the most common needs of uses the concept of Axis in XPath, without you writing an XPath.

**Coded Axes Locator**
----------------------

In code, you use Arjuna's **axes** pbject to define axes with a start node (See :ref:`node_locator`) as the argument to its constructor. Then you can use its builder methods for directions and specifying node in each direction.

.. code-block:: python

    app.element(axes=axes(node(id="user_login")).up(node(tags="label")))

In the above code, you specify that the node (See :ref:`node_locator`) with id user_login is the starting point. From there, move in the up direction (towards ancestors) and find a GuiWidget with label tag.

You can use any of the directions - **up**, **down**, **left** or **right** in the same manner. 

You can chain the directions as well:

.. code-block:: python

    app.element(axes=axes(node(id="user_login")).up(node(tags="form")).down(node(classes="button)))

**GNS Axes** (Unique Directions)
--------------------------------

In GNS, you represent axes locator as a YAML dict with a **start** key and one more of **up**, **down**, **left** or **right** keys.

The values for these keys are equivalent of :ref:`node_locator`.

.. code-block:: yaml

  axes1:

    axes:
      start:
        id: user_login
      
      up:
        tags: label

  axes_dir_multi:

    axes:
      start:
        id: user_login
      
      up:
        tags: form

      down:
        classes: button

**GNS Axes** (Repeated Directions)
----------------------------------

If in GNS, you want to repeat the directions, then instead of axes specification as a dictionary you can use the YAML list format:

.. code-block:: yaml

    axes_dir_repeat:

        axes:

            - start:
                tags: html
            
            - down:
                classes: button

            - up:
                tags: form

            - down:
                tags: p

            - right:
                tags: p

            - left:
                tags: p

            - down:
                tags: input
