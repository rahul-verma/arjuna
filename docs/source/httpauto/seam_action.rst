.. _seam_action:

**SEAMful - Action**
====================

Introduction
------------

Arjuna's **HttpService** object can read and send abstracted Http actions in YAML based externalization files.

An HTTP action can define:
    - A sequence of messages to be sent.
    - Data (hardcoded or parameterized) to be shared with multiple messages.

Defining **Actions** with **Anonymous Service**
-----------------------------------------------

The action files are placed under **<Arjuna Test Project root dir>/httpauto/action** directory.

    .. code-block:: yaml

        myproj
          - httpauto
            - action
              - myact1.yaml
              - myact2.yaml
            - message
              - mymsg1.yaml
              - mymsg2.yaml

In this mode, in an action file you can refer to all messages defined in **<Arjuna Test Project root dir>/httpauto/message** directory by name.

Defining **Actions** with **Named Service**
-------------------------------------------

The message files are placed under **<Arjuna Test Project root dir>/httpauto/service/<service_name>/action** directory.

    .. code-block:: yaml

        myproj
          - httpauto
            - service
              - myservice
                - action
                  - myact1.yaml
                  - myact2.yaml
                - message
                  - mymsg1.yaml
                  - mymsg2.yaml

In this mode, in an action file you can refer to all messages defined in **<Arjuna Test Project root dir>/httpauto/service/<service_name>/message** directory by name.

Sending **Action using Service**
--------------------------------
Depending on whether the action file name is a valid Python name or not, you can use the following ways to send this HTTP action using the service:

    .. code-block:: python

        # Python name
        service.action.myact1.perform()

        # Python name
        service.perform("non python name")
        service.perform("non/python/name") # With sub-directories

The service will look for the correspinding action in **<Arjuna Test Project root dir>/httpauto/action** or **<Arjuna Test Project root dir>/httpauto/service/<service_name>/action** directory depending on whether it is an anonymous service or named service respectively.

It will then perform the corresponding HTTP action as per specification.

Performing **Sequence of HTTP Messages without HTTP Action Abstraction**
------------------------------------------------------------------------

To understand the importance of HTTP Action abstraction, let's assume that it is not available.

A real test at HTTP layer takes more than one interaction/message.

Let's say you have four messages defined in 4 separate files:
    - Check items list being empty

        .. code-block:: yaml

            # Message file: items_empty.yaml

            request:
                method: get
                route: "/items"

            codes: 200

            validate:
                content:
                    empty: True

    - Post an item

        .. code-block:: yaml

            # Message file: item_post.yaml

            label: Check creating of item

            request:
                method: post
                route: "/item"
                content_type: json
                content: {
                    'name': "$name$",
                    'price': "$price$"
                }

            codes: 200

    - Check that items list is now non-empty

        .. code-block:: yaml

            # Message file: items_non_empty.yaml

            label: Check Item List

            request:
                method: get
                route: "/items"

            content_type: json

            validate:
                content:
                    empty: False

    - Get the item based on ID.

        .. code-block:: yaml

            # Message file: item_get.yaml

            label: Check fetching of item

            request:
                method: get
                route: "/item/$name$"

            content_type: json

            match:
                content: {
                    'name': "$name$",
                    'price': "$price$"
                }

            codes: 200

Note that these 4 messages, you need to parameterize the following:
    * name
    * price

In the absence of concept of HTTP action, you will do something like following with HTTP message abstraction:

    .. code-block:: python

        name = Random.ustr()
        input_dict = {'name': name, 'price': 1}
        service.message.items_empty.send()
        service.message.item_post.send(name=input_dict['name'], price=input_dict['price'])
        service.message.items_non_emtpty.send()
        service.message.item_get_1.send(name=input_dict['name'], price=input_dict['price'])

**Basic HTTP Action File**
--------------------------

Let's define a basic action file which just contains the sequence of these messages:

    .. code-block:: yaml

        # Action file: create_first_item.yaml

        messages:
            - items_empty
            - item_post
            - items_non_empty
            - item_get

**Performing HTTP Action**
--------------------------

To perform an action, you use **<service_obj>.action.<action_name>.peform** method. You can pass arbitrary arguments to format data placeholders.

    .. code-block:: python

        name = Random.ustr()
        input_dict = {'name': name, 'price': 1}
        service.action.create_first_item.perform(name=input_dict['name'], price=input_dict['price'])

Using **Flattened Dictionary** for Data
---------------------------------------

If you use dictionary keys wisely i.e. parameter names are same as dictionary keys:

    .. code-block:: python

        name = Random.ustr()
        input_dict = {'name': name, 'price': 1}
        service.action.create_first_item.perform(**input_dict)

Using **Flattened Data Entity** for Data
----------------------------------------

You can similarly use a data enity as well, which gives an even better looking terse code:

    .. code-block:: python

        item = Item()
        service.action.create_first_item.perform(**item)

Using **data** Formatting Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rather than passing individual arguments, you can also use the special **data** container as well.

Dictionary example:

    .. code-block:: python

        name = Random.ustr()
        input_dict = {'name': name, 'price': 1}
        service.action.create_first_item.perform(data=input_dict)

Data Entity example:

    .. code-block:: python

        service.action.create_first_item.perform(data=Item())

Using **Data Defined in Action File**
-------------------------------------

Rather than passing data from outside, you can define data in action file too. This data itself can be dynamic.

For example:

    .. code-block:: yaml

        data:
            name:
                generator: ustr
            price: 
                generator: fixed_length_number
                length: 3

In the above code we see that under **data** section, **name** and **price** have been defined.

    * **name** has been defined as a **ustr** which is equivalent of **Random.ustr()**.
    * **name** has been defined as a **fixed_length_number** with arg **length** as 3, which is equivalent of **Random.fixed_length_number(length=3)**.

You can use any of the :py:class:`Random <arjuna.tpi.data.generator.Random>` class methods to create data.

These can be used in message files with placeholders **$name$** and **$price**. You can also use full qualified names: **$data.name$** and **$data.price$**.

Correspondingly, Python code for action is simpler:

    .. code-block:: python

        service.action.create_first_item.perform()

Creating and Using **Data Entity in Action File**
-------------------------------------------------

You can also create objects of Data Entities if you have defined them as a hook. Refer :ref:`data_entity_injectable`.

For example, if we have an entity Item in **project/lib/hook/entity.py** python file.

    .. code-block:: python

        from arjuna import *

        Item = data_entity(
            "Item",
            name = Random.ustr,
            price = generator(Random.fixed_length_number, length=3)

In the action file, you can create an object of this entity very easily using **entity** construct:

    .. code-block:: yaml

        entity:
            item: Item

In messages, you can use **item** as a full data entity or attributes of it using **item.name** and **item.price**.

Correspondingly, Python code for action is simpler:

    .. code-block:: python

        service.action.create_first_item.perform()

Creating **Aliases for Data**
-----------------------------

At times you want to create aliases for data. This can be done in **store** constuct.

In the following example, **id** is an alias for **name**:

    .. code-block:: yaml

        data:
            name:
                generator: ustr
            price: 
                generator: fixed_length_number
                length: 3

        alias:
            id: name

In the following example, we see a more involved alias, where **id** is an alias for data entity **item**'s **name** attribute.

    .. code-block:: yaml

        entity:
            item: Item

        alias:
            id: item.name

Correspondingly, Python code for action is simpler:

    .. code-block:: python

        service.action.create_first_item.perform()


**Extracting and Using Data From One Message to Another**
---------------------------------------------------------

We can extract and store data in SEAMful Message files. Refer :ref:`message_data_extraction`.

Such data can be used within the message file for validations.

You can also use this data in the subsequent messages in action file.

Let's consider a user flow:
    * Using a POST request you create an item. The response contains a unique id **iid** for this newly created item. We use the **store** construct to extract it based on Json Path.

        .. code-block:: yaml

            # ditem_post.yaml

            label: Check creatiion of dynamic item

            request:
                method: post
                route: "/ditem"
                content_type: json
                content: {
                    'name': "$name$",
                    'price': "$price$"
                }

            store:
                iid:
                    jpath: iid

            codes: 200

    * In subsequent GET request you use this **iid** to retrieve and validate whether the new item was created correctly. We use placeholder **$iid$** to use the newly created unique identifier for item.

        .. code-block:: yaml

            # ditem_get.yaml

            label: Check dynamic item fetching

            request:
            method: get
            route: "/ditem/$iid$"

            content_type: json

            match:
            content: {
                'iid': $iid$,
                'name': "$name$",
                'price': "$price$"
            }

            codes: 200

And here's the action file. It provides the initial data and lets **iid** flow between the messages automatically:

    .. code-block:: yaml

        # ditem_create.yaml

        data:
            name:
                generator: ustr
            price: 
                generator: fixed_length_number
                length: 3

        messages:
            - ditem_post
            - ditem_get
