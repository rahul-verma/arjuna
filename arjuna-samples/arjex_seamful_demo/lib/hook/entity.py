from arjuna import *

Item = data_entity(
    "Item",
    name = Random.ustr,
    price = Random.fixed_length_number(length=3)
)

