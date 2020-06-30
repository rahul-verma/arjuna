.. _datagen_entity:


**Random Data** Generation
--------------------------

Data Generation is a common need in testing and test automation.

Python's own libaries can be used for generation of random strings and numbers. However, tester's needs are much more involved than that.

Arjuna currently has basic support for contextual data generation by using **mimesis** library provided by its :py:class:`Random <arjuna.tpi.engine.data.generator.Random>` class.

Using its methods you can generate the following:

    * first_name
    * last_name
    * name
    * city
    * country
    * email
    * phone
    * house_number
    * street)name
    * street_number
    * postal code
    * sentence
    * ustr
    * fixed_length_number


Creating a Basic **Data Entity**
--------------------------------

Arjuna's :py:class:`data_entity <arjuna.tpi.data.entity.data_entity>` gives you an advanced, yet easy way of creating entities that contain associated generated/provided data.

In simple words, a Data Entity is a Python class whose objects when created can contain automatically generated associated data.

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















