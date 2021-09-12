.. _data_builtin_entities:

**Built-in Complex Random Data Entities**
=========================================

Rather than generating one piece of data at a time, you can also use some of the randomly generated data entities that are provided by Arjuna.

**Person**
----------

**Random.person** method generates various aatributes that can be used while providing data for a person.

.. code-block:: python

    person = Random.person()

It will create a **Person** entity like the one shown below:

    .. code-block:: python

        Person(
            qualification=PhD, 
            age=49, 
            blood_type=AB+, 
            email=defoliant1918@outlook.com, 
            first_name=Karima, 
            last_name=Noel, 
            name=Karima Noel, 
            gender=Fluid, 
            height=1.68, 
            id=50-97/16, 
            language=Polish, 
            nationality=Guatemalan, 
            occupation=Applications Engineer, 
            phone=1-848-014-0783, 
            title=Mr., 
            university=University of West Florida (UWF), 
            weight=53, 
            work_experience=27
        )

You can choose to override any of the values using any of the following, just like you do when creating any data entity:
    * Any Python Object
    * A Python callable
    * Arjuna `generator`
    * Arjuna `composite`

    .. code-block:: python

        person = Random.person(occupation="Software Tester")


**Address**
-----------

**Random.address** method generates various aatributes that can be used while providing data for an address.

    .. code-block:: python

        address = Random.address()

It will create an **Address** entity like the one shown below:

    .. code-block:: python

        Address(
            calling_code=+44, 
            city=Chesterfield, 
            country=United States, 
            country_code=SO, 
            latitude=-43.899334, 
            longitude=12.852834, 
            postal_code=99613, 
            state=California, 
            street_name=Faxon, 
            street_number=7, 
            street_suffix=High Street
        )

You can choose to override any of the values using any of the following, just like you do when creating any data entity:
    * Any Python Object
    * A Python callable
    * Arjuna `generator`
    * Arjuna `composite`

    .. code-block:: python

        person = Random.address(street_name="Eat Street")








