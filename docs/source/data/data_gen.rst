.. _data_gen:

**Random Data Generation**
==========================

Arjuna's **Random** Class
-------------------------

Data Generation is a common need in testing and test automation.

Python's own libaries can be used for generation of random strings and numbers. However, tester's needs are much more involved than that.

Arjuna currently has basic support for contextual data generation by using **mimesis** library provided by its :py:class:`Random <arjuna.tpi.data.generator.Random>` class.

Using class methods of :py:class:`Random <arjuna.tpi.data.generator.Random>` you can generate the following:

Random **Person** Data
----------------------

First Name
^^^^^^^^^^
You can generate a random first name with :py:func:`first_name <arjuna.tpi.data.generator.Random.first_name>`.

    .. code-block:: python

        Random.first_name()

Last Name
^^^^^^^^^^
You can generate a random last name with :py:func:`last_name <arjuna.tpi.data.generator.Random.last_name>`.

    .. code-block:: python

        Random.last_name()

Full Name
^^^^^^^^^^
You can generate a random full name with :py:func:`name <arjuna.tpi.data.generator.Random.name>`.

    .. code-block:: python

        Random.name()

Email
^^^^^
You can generate a random syntactically valid country name with :py:func:`email <arjuna.tpi.data.generator.Random.email>`.

    .. code-block:: python

        # Generate complete email address
        Random.email()

        # Generate name part of the email address and use provided domain
        Random.email(domain="test.com")

        # Generate domain part of the email address and use provided name
        Random.email(name="test")

        # For some logical reason (where name and domain are bein data driven), if you want to provide both (no randomness)
        Random.email(name="test", domain="test.com")

Phone
^^^^^
You can generate a random syntactically valid phone number with :py:func:`phone <arjuna.tpi.data.generator.Random.phone>`.

    .. code-block:: python

        Random.phone()

Random **Address** Data
-----------------------

City
^^^^
You can generate a random valid city name with :py:func:`city <arjuna.tpi.data.generator.Random.city>`.

    .. code-block:: python

        Random.city()

Country
^^^^^^^
You can generate a random valid country name with :py:func:`country <arjuna.tpi.data.generator.Random.country>`.

    .. code-block:: python

        Random.country()

House Number
^^^^^^^^^^^^
You can generate a random house number with :py:func:`house_number <arjuna.tpi.data.generator.Random.house_number>`.

    .. code-block:: python

        # Something like 1043
        Random.house_number()

        # Something like H.No. 1043. Space is added by default to prefix.
        Random.house_number(prefix="H.No.")

Street Name
^^^^^^^^^^^
You can generate a random street name with :py:func:`street_name <arjuna.tpi.data.generator.Random.street_name>`.

    .. code-block:: python

        Random.street_name()

Street Number
^^^^^^^^^^^^^
You can generate a random street number with :py:func:`street_number <arjuna.tpi.data.generator.Random.street_number>`.

    .. code-block:: python

        # Something like 43
        Random.street_number()

        # Something like St 43. Space is added by default to prefix.
        Random.street_number(prefix="St")

Postal Code
^^^^^^^^^^^
You can generate a random valid postal code with :py:func:`postal_code <arjuna.tpi.data.generator.Random.postal_code>`.

    .. code-block:: python

        Random.postal_code()

Random **Text**
---------------

Sentence
^^^^^^^^
You can generate a random sentence with :py:func:`sentence <arjuna.tpi.data.generator.Random.sentence>`.

    .. code-block:: python

        Random.sentence()

Unique String
^^^^^^^^^^^^^
You can generate a random unique string with :py:func:`ustr <arjuna.tpi.data.generator.Random.ustr>`.

This is a very advanced unique string generator with various options.

    .. note::

        Arjuna uses the following math to calculate base string length:

            .. code-block:: text

                length of prefix + delim length + 36 (length of uuid4)

        Different arguments tweak the length of generated string by appending uuid one or more times fully or partially.

    .. note::

        When prefix is not provided, delimiter is ignored as well.

    .. code-block:: python

        # Generates a uuid4 string of length 36. E.g. f9bc6834-f712-4caa-a950-85e5413e9a29
        Random.ustr()

        # Generates a uuid4 string of length 36 with prefix "abc". Default delimiter is "-". 
        # E.g. abc-f9bc6834-f712-4caa-a950-85e5413e9a29
        Random.ustr(prefix="abc")

        # Generates a uuid4 string of length 36 with prefix "abc" with delimiter is "::". 
        # E.g. abc::f9bc6834-f712-4caa-a950-85e5413e9a29
        Random.ustr(prefix="abc", delimiter="::")

        # Generate a string with minimum length. Leads to truncation or repetition of generated uuid4 string depending on length specified.

        # Truncation 
        # E.g. 8d19b972-27ea-4943-9257-3de218c95110
        Random.ustr(minlen=17)

        # Repetition 
        # E.g. 1de95392-1a59-4ca7-b61a-d794907ef30e1de95392-1a59-4ca7-b61a-d794907ef30e1de95392-1a59-4ca7-b61a-d794907ef30e1de9
        Random.ustr(minlen=71) 

        # You can also put an upper limit on length of string
        # E.g. 660af049-2ebd-4bb9-8
        Random.ustr(maxlen=20) 
        # E.g. fce87459-f257-48a1-bd48-019a0e862590fce87459-f257-48a1-bd48
        Random.ustr(maxlen=67) 

        # Using minlen and maxlen together
        # E.g. 4a28a3ca-1f22-47d5-8c44-da333e0adfd04a2
        Random.ustr(minlen=32, maxlen=70)  

        # Using all provisions together
        # E.g. abc*ca88198f-bd07-4b1d-83f4-a83e4e6ece8bca88198f-bd07-4b1d-83f4-a83e4e6ece8bc
        Random.ustr(prefix="abc", delim="*", minlen=60, maxlen=85) 


This method has a **strict** mode to guarantee uniqueness of string. If True uniqueness of string is enforced which means full generated uuid must be used atleast once. This means length of generated string must be >= base string length, else an exception is thrown.

    .. code-block:: python

        Random.ustr(prefix="abc", delim="*", maxlen=24, strict=True) # exception

Fixed Length String
^^^^^^^^^^^^^^^^^^^
You can generate a random fixed length string with :py:func:`fixed_length_str <arjuna.tpi.data.generator.Random.fixed_length_str>`.

    .. code-block:: python

        Random.fixed_length_str(length=10)

Alphabet
^^^^^^^^
You can get complete alphabet as list of characters with :py:func:`alphabet <arjuna.tpi.data.generator.Random.alphabet>`.

    .. code-block:: python

        Random.alphabet()

        # In lower case
        Random.alphabet(lower_case=True)

Random **Number**
-----------------

Integer
^^^^^^^
You can generate a random integer with :py:func:`int <arjuna.tpi.data.generator.Random.int>`.

    .. code-block:: python

        # Generate an integer between 0 to 10
        Random.int(10)
        Random.int(end=10)

        # Generate an integer between 5 to 10  
        Random.int(10, begin=5)
        Random.int(begin=5, end=10)  

Fixed Length Number
^^^^^^^^^^^^^^^^^^^
You can generate a random fixed length number with :py:func:`fixed_length_number <arjuna.tpi.data.generator.Random.fixed_length_number>`.

    .. code-block:: python

        Random.fixed_length_number(length=9)

Random **Color**
----------------

Color
^^^^^
You can generate a random color with :py:func:`color <arjuna.tpi.data.generator.Random.color>`.

    .. code-block:: python

        # Generate an random color. E.g. Red
        Random.color()

RGB Color
^^^^^^^^^
You can generate a random RGB color with :py:func:`rgb_color <arjuna.tpi.data.generator.Random.rgb_color>`.

    .. code-block:: python

        # Generate an random color. E.g. (68, 233, 85)
        Random.rgb_color()

Hex Color
^^^^^^^^^
You can generate a random hex color code with :py:func:`int <arjuna.tpi.data.generator.Random.color>`.

    .. code-block:: python

        # Generate an random color. E.g. #5dabcf
        Random.hex_color()

**Localizing Random Data**
--------------------------

At times you need the randomly generated data localized to make it more natuarl or even valid.

Following generators in Random class can be passed **locale** argument for generating localized data:

    * :py:func:`first_name <arjuna.tpi.data.generator.Random.first_name>`
    * :py:func:`last_name <arjuna.tpi.data.generator.Random.last_name>`
    * :py:func:`name <arjuna.tpi.data.generator.Random.name>`
    * :py:func:`phone <arjuna.tpi.data.generator.Random.phone>`
    * :py:func:`email <arjuna.tpi.data.generator.Random.email>`
    * :py:func:`street_name <arjuna.tpi.data.generator.Random.street_name>`
    * :py:func:`street_number <arjuna.tpi.data.generator.Random.street_number>`
    * :py:func:`house_number <arjuna.tpi.data.generator.Random.house_number>`
    * :py:func:`postal_code <arjuna.tpi.data.generator.Random.postal_code>`
    * :py:func:`city <arjuna.tpi.data.generator.Random.city>`
    * :py:func:`country <arjuna.tpi.data.generator.Random.country>`
    * :py:func:`sentence <arjuna.tpi.data.generator.Random.sentence>`

Using **locale** Argument
^^^^^^^^^^^^^^^^^^^^^^^^^

You can pass the locale argument of a generator method and pass a **DataLocale** object which can be easily created using Random class.

For example, for French locale, you can use

    .. code-block:: python

        Random.locale.fr

You can pass this object to a Random generator method using the locale argument. Here's the example of **Random.first_name**:

    .. code-block:: python

        Random.first_name(locale=Random.locale.fr)

As an example, following are some random first names genererated as a result of **Random.first_name** call and looping for all locales:

    .. code-block:: text

        cs: Armand
        da: Osmund
        de: Frederika
        de_at: Faiga
        de_ch: Küni
        el: Σάκης
        en: Patricia
        en_gb: Almeta
        en_au: Madalene
        en_ca: Valérie
        es: Joaquin
        es_mx: Salvatore
        et: Ulmar
        fa: آریانوش
        fi: Mika
        fr: Mathias
        hu: Hieronima
        is: Siguróli
        it: Benedetto
        ja: 舞
        kk: Ақберді
        ko: 대원
        nl: Iris
        nl_be: Johanna
        no: Conny
        pl: Aleksandra
        pt: Ribca
        pt_br: Brice
        ru: Зульмира
        sv: Svenborg
        tr: Feyza
        uk: Радован
        zh: 灵攘

.. _suppored_data_locales:

**Supported locales**
^^^^^^^^^^^^^^^^^^^^^

Arjuna :py:class:`Random <arjuna.tpi.data.generator.Random>` class supports the locales supported by **mimemis** library. Following are the supported 33 locales as taken from official documentation of **mimesis** :

=========         ====================    ====================
Code              Name                    Native Name
=========         ====================    ====================
**cs**            Czech                   Česky
**da**            Danish                  Dansk
**de**            German                  Deutsch
**de_at**         Austrian german         Deutsch
**de_ch**         Swiss german            Deutsch
**el**            Greek                   Ελληνικά
**en**            English                 English
**en_au**         Australian English      English
**en_ca**         Canadian English        English
**en_gb**         British English         English
**es**            Spanish                 Español
**es_mx**         Mexican Spanish         Español
**et**            Estonian                Eesti
**fa**            Farsi                   فارسی
**fi**            Finnish                 Suomi
**fr**            French                  Français
**hu**            Hungarian               Magyar
**is**            Icelandic               Íslenska
**it**            Italian                 Italiano
**ja**            Japanese                日本語
**kk**            Kazakh                  Қазақша
**ko**            Korean                  한국어
**nl**            Dutch                   Nederlands
**nl_be**         Belgium Dutch           Nederlands
**no**            Norwegian               Norsk
**pl**            Polish                  Polski
**pt**            Portuguese              Português
**pt_br**         Brazilian Portuguese    Português Brasileiro
**ru**            Russian                 Русский
**sv**            Swedish                 Svenska
**tr**            Turkish                 Türkçe
**uk**            Ukrainian               Українська
**zh**            Chinese                 汉语
=========         ====================    ====================

You can also get a dictionary of locale name and descriptive name as follows:

    .. code-block:: python

        Random.locale.supported
