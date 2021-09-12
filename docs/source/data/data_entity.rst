.. _data_entity:

**Data Entities**
=================

In simple words, a Data Entity is a Python class whose objects when created can contain automatically generated associated data.

Creating a Basic **Data Entity**
--------------------------------

Arjuna's :py:class:`data_entity <arjuna.tpi.data.entity.data_entity>` gives you an advanced, yet easy way of creating entities that contain associated generated/provided data.

In its simplest form, :py:class:`data_entity <arjuna.tpi.data.entity.data_entity>` is a Python class (without custom behaviors/methods) creator without writing a class. In its more involved forms, it starts serving complex data needs of today's automation world.

In the rest of this page, more advanced options will be considered. Here's a simple example of a Data Entity with static data:

    .. code-block:: python

        # Provide name of entity and names of desired data attributes as strings
        Person = data_entity("Person", "name", "age", "country")

        # Or provide names of data attributes as a single string (space separated)
        Person = data_entity("Person", "name age country")

        # Now you can use it as a regular Python class as if the data attributes are keyword arguments in class definition.
        person = Person(name="Ravi", age=25, country="India")

        # Access Data
        person.name
        person.age
        person.country

This might look fancy to the novice, however so far there is nothing special about it. You could have achieved the above by using **namedtuple** which is available in Python's built-in **collections** module.

Next sections tell you what makes **data_entity** special.

Setting Defaults in Data Entity
-------------------------------

You can define data attributes with default value in the familiar Pythonic way for keyword arguments:

    .. code-block:: python

        Person = data_entity("Person", "name age", country='India')

Data Entity has a **Python Dictionary-like Behavior**
-----------------------------------------------------
Data entity objects behave like Python dictionaries. 


Attribute as a Key
^^^^^^^^^^^^^^^^^^

You can retrieve an attribute value as:

    .. code-block:: python
    
        entity.attr
        # or
        entity['attr']

**keys** and **items** Methods - None values Removed by Default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following dict-like operations are valid too. The key difference to note is that in these operations that attributes that have None value are excluded unlike a Python dictionary.

    .. code-block:: python

        entity.keys()
        entity.items()
        **entity # Unpacking of key-values

        # Iterating on keys
        for attr in entity:
            pass

        # Iterating on key-value pairs
        for attr, value in entity.items():
            pass

**keys** and **items** Methods - Retaining None Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To retain keys/attrs corresponding to None values, you can provide **remove_none=False** as argument:

    .. code-block:: python

        entity.keys(remove_none=False)
        entity.items(remove_none=False)
        **entity # Unpacking of key-values

        # Iterating on keys
        for attr in entity.keys(remove_none=False):
            pass

        # Iterating on key-value pairs
        for attr, value in entity.items(remove_none=False):
            pass

**len** unction vs **size** Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Also note that because len() in Python is not flexible to allow for the above, you can use **size** method:

    .. code-block:: python

        len(entity) # Will ignore attrs with None value
        entity.size() # Will ignore attrs with None value
        entity.size(remove_none=False) # Includes attrs with None value

**remove** Argument for Removing Specific Keys/Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All above mentioned methods also accept **remove** argument to explicitly exclude one or more attributes by name.

    .. code-block:: python

        entity.keys(remove='some_key')
        entity.keys(remove={'some_key1', 'some_key2'})

        entity.items(remove='some_key')
        entity.items(remove={'some_key1', 'some_key2'})

        entity.size(remove='some_key')                 
        entity.size(remove={'some_key1', 'some_key2'})

**del** is NOT Allowed
^^^^^^^^^^^^^^^^^^^^^^

Delete operation is disllowed on the data entity because it corresponds to attribute deletion. Use **as_dict()** method for representation that has one or more keys removed.

    .. code-block:: python

        # Raises exception
        del entity['some_attr']


Creating **Immutable** Data Entity Objects
------------------------------------------

You can make an object of a data entity IMMUTABLE by passing **freeze=True** argument.

    .. code-block:: python

        person = Person(name="SomeName", age=21, freeze=True)
        # Raises Exception
        person.age = 25


Basic Usage of **Random** with **Data Entity**
----------------------------------------------

You can club the usage of **Random** class with Data Entity to create an object with random data:

    .. code-block:: python

        Person = data_entity("Person", "name age country")
        person = Person(name=Random.name, age=Random.int(begin=18, end=65), country=Random.country)


**Dynamic Generation of Data** for **Data Entities**
----------------------------------------------------

Using **Callables** in **Random** Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the point where the true power of Data Entities starts to unfold.

You can associate a Data Entity's attribute with a callable to generate unqiue data for each object of this Data Entity.

    .. code-block:: python

        Person = data_entity("Person", "name age", country=Random.country)

        # Gets assigned a random country when object is created 
        person1 = Person(name=Random.name, age=Random.int(end=65))

        # Gets assigned a random country when object is created 
        person2 = Person(name=Random.name, age=Random.int(end=65))

Using **User-Defined Callables**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also use your own random data generator callables:


    .. code-block:: python

        def some_data_gen():
            return random.randint(20,60)

        Person = data_entity("Person", "name country", age=some_data_gen)

        # Gets assigned a random int as age when object is created, as returned by some_data_gen
        person1 = Person(name=Random.name, country='India')

        # Gets assigned a random int as age when object is created as returned by some_data_gen
        person2 = Person(name=Random.name, country='India')

.. _generator:

Arjuna's **generator** Construct
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna's **generator** construct can call any callable with provided arbitrary positional as well as keyword arguments.

This is a **lazy mechanism**. It means that when this construct is used, till its **generate()** call is made, the corresponding callable is not called.

Following are some examples

    .. code-block:: python

        generator(Random.first_name).generate()
        generator(some_callable, arg1, arg2, kwarg1=value1, kwarg2=value2).generate()

Using **generator** Construct to Provide Arbitrary Arguments to Generator Callables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data generator functions could take any positional arguments and/or keyword arguments.

Data Entities accept Arjuna's **generator** construct to support this advanced facility.

You can use it with your own functions as well. Here's an example with `Random.int` function:


    .. code-block:: python

        Person = data_entity("Person", "name country", age=generator(Random.int, begin=18, end=65))

Processing Dynamically Generated Data
-------------------------------------

Basic **Processor** Callable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might want to process the generated data before making it a part of Data Entity. You can do it by passing a **converter** callable to **generator**:

    .. code-block:: python

        def lower(in_str):
            return in_str.lower()

        Person = data_entity("Person", "age country", name=generator(Random.name, processor=lower))

Here if the generated name is "Ravi Sharma", it will stored as "ravi sharma" in the data entity post conversion.

**Processor** Callable as a Method of Generated Data Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the processor is a string, it is assumed to be a method of the generated data object and called:

    .. code-block:: python

        Person = data_entity("Person", "age country", name=generator(Random.name, processor="lower"))


Defining **Processor** Callable with Arbitrary Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **generator** constructs also accepts Arjuna's **processor** construct for advanced usage:

    .. code-block:: python

        def replace_space(in_str, char=":"):
            return in_str.replace(" ", char)

        processor = processor(replace_space, char="-")
        Person = data_entity("Person", "age country", name=generator(Random.name, processor=processor))

If the callable provided to **processor** is a string, it is assumed to be a method of the generated data object and called.


Defining **Composite Data** Using **composite** and **composer** Constructs
---------------------------------------------------------------------------

At times, you might want to club data obtained from multiple generators. You might want to combine some static data with it as well, as needed.

Data Entities in Arjuna accept Arjuna's **composite** construct for data attributes.

Once the data is available as a single sequence, it is composed together using the **composer** callable that you can optionally provide, else the same sequence is stored as the value for this data attribute.

If you have reached this stage, it is assumed, that you know what you are doing. So, here's a complete example demonstrating everything a Data Entity has to offer:

    .. code-block:: python

        def to_upper_case(data_str):
            return data_str.upper()

        def join(in_list, char=":"):
            return char.join(in_list)

        processor = processor(replace_space, char="-")
        Person = data_entity("Person", 
                age = generator(Random.int, begin=18, end=65),
                country = Random.country,
                name=composite(
                        "Mz",
                        generator(Random.first_name, processor="upper"),
                        generator(Random.last_name, processor=to_upper_case),
                        composer=composer(join, char=" ")
                    )
                )


**Creating a Data Entity from Other Data Entities**
---------------------------------------------------

You might want to create a data entity from existing data entities and have the option to add more attributes as well as override behavior of existing ones.

To achieve this you can make use of the **bases** argument. A single base entity can be passed as a string. Multiple base entities can be passed as a list or tuple.

**Single Base Data Entity**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider the following base data entity:

    .. code-block:: python

        # Simple base with one mandatory and one optional attr
        Person = data_entity("Person", "age", fname=Random.first_name)

In the following sections, we will utilize this as base entity and make further tweaks.

**Adding** a **Mandatory** Attribute
""""""""""""""""""""""""""""""""""""

Here the **UpdatedPerson** entity uses **Person** as its base entity and adds **gender** as a mandatory attribute:

    .. code-block:: python

        # Top entity adds a mandatory attr
        UpdatedPerson = data_entity("UpdatedPerson", "gender", bases=Person)
        p1 = UpdatedPerson(gender="M", age=20)
        p2 = UpdatedPerson(gender="M", age=20, fname="Roy")


**Adding** an **Optional/Default** Attribute
""""""""""""""""""""""""""""""""""""""""""""

Here the **UpdatedPerson** entity uses **Person** as its base entity and adds **city** as an optional attribute:

    .. code-block:: python

        # Top entity adds an optional attr
        UpdatedPerson = data_entity("UpdatedPerson", city=Random.city, bases=Person)
        p1 = UpdatedPerson(age=20, fname="Roy")
        p2 = UpdatedPerson(age=20, fname="Roy", city="Bengaluru")


**Changing Value of Optional/Default Attribute**
""""""""""""""""""""""""""""""""""""""""""""""""

Here the **UpdatedPerson** entity uses **Person** as its base entity and changes the value for **fname** attribute.

    .. code-block:: python

        # Top entity adds an optional attr
        UpdatedPerson = data_entity("UpdatedPerson", fname=Random.name, bases=Person)
        p1 = UpdatedPerson(age=20)
        p2 = UpdatedPerson(age=20, fname="Roy")


Converting an **Optional/Default Attribute to Mandatory Attribute**
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Here the **UpdatedPerson** entity uses **Person** as its base entity and makes **fname** mandatory.

    .. code-block:: python

        # Top entity adds an optional attr
        UpdatedPerson = data_entity("UpdatedPerson", "fname", bases=Person)
        p1 = UpdatedPerson(age=20, fname="Roy")


Converting a **Mandatory Attribute to Optional Attribute**
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Here the **UpdatedPerson** entity uses **Person** as its base entity and makes **age** attribute optional.

    .. code-block:: python

        # Top entity adds an optional attr
        UpdatedPerson = data_entity("UpdatedPerson", age=generator(Random.fixed_length_number, length=2), bases=Person)
        p1 = UpdatedPerson()

**Multiple Base Data Entities**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also assign multiple base data entities.

**Simple Merged Data Entity**
"""""""""""""""""""""""""""""

One simple requirement you might have is to merge two data entities together.

Here's an intuitive approach:

    .. code-block:: python

        Person = data_entity("Person", "age", fname=Random.first_name)
        Address = data_entity("Address", city=Random.city, country=Random.country, postal_code=Random.postal_code)

        # Merged Entity
        PersonWithAddress = data_entity("PersonWithAddress", bases=(Person, Address))
        p = PersonWithAddress(age=40)

**Merged Data Entity with Custom Overrides**
""""""""""""""""""""""""""""""""""""""""""""

Sometimes the base data entities have common attributes and the top data entity also might choose to change the behaviors for more complex requirements.

Following code snippet demonstrates this:

    .. code-block:: python

        # Simple Base 1 with one mandatory and one optional attr
        Person = data_entity("Person", "age", fname=Random.first_name)

        # Base 2 adds one mandatory arg, makes fname mandatory, adds one optional arg
        MiddlePerson = data_entity("MiddlePerson", "gender fname", city=Random.city, bases=Person1)

        # Top entity makes age optional, add one mandatory parameter
        TopPerson = data_entity("TopPerson", "country", age=generator(Random.fixed_length_number, length=2), bases=(Person, MiddlePerson))
        p1 = TopPerson(gender="M", fname="Roy", country="India")
        p2 = TopPerson(gender="M", fname="Roy", age=15, country="India")

.. _data_entity_injectable:

Defining Entities for **Dependency Injection**
----------------------------------------------

If you define a data entity that are imporatble as **from yourproject.lib.hook.entity import MyEntity**, then Arjuna can allow the usage of this entity in places where it can do dependency injection.

Currently, following places allow for dependency injection for a Data Entity:
    * SEAMful HTTP Action yaml files

In its simplest form, you can code an entity in **project/lib/hook/entity.py** python file. For example:

    .. code-block:: python

        from arjuna import *

        Item = data_entity(
            "Item",
            name = Random.ustr,
            price = generator(Random.fixed_length_number, length=3)