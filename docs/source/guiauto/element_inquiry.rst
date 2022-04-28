.. _element_state_wait:

**Inquiring Element Information**
=================================

**Inquiring HTML Source** of an Element
---------------------------------------

Arjuna provides source code of an element using the **source** property.

.. code-block:: python

   source = element.source

   # The source object can be used to get a lot of information

   source.tag # Tag name
   source.attrs # Attributes key-values as a dictionary
   source.is_attr_present("somename") 
   source.get_attr_value("somename") # Raises exception if attribute is not Found.
   source.get_attr_value("somename", optional=True) # Returns None if attribute is not Found.
   source.value # Content of 'value' attribute. Raises exception if 'value' attribute is not Found.
   source.get_value() # Content of 'value' attribute. Raises exception if 'value' attribute is not Found.
   source.get_value(optional=True) # Content of 'value' attribute. Returns None if attribute is not Found.
   
**Inquiring Properties and Attributes** an Element
--------------------------------------------------

As seen above, you can use element's source to inquire attributes. You can also do this directly using the element:

.. code-block:: python

   source = element.get_attr("abc")

Browsers store more information about elements than what can be seen in HTML attributes.

Such properties can be inquired as follows:

.. code-block:: python

   source = element.get_property("abc")





