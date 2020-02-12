### Arjuna's Value abstraction

A test engineer deals with various types of objects while writing an automated test. 

As a part of the same, there are various object operations needed, type conversion being one of them. Beyong simple type conversions, at times it is about splitting of a string, creating an Enum etc.

Just like other programming languages, depend on the nature of operation, Python has different ways of achieving these related operations. 

The purpose of Value abstraction is to provide a single interface for all these needs.

Understanding Value is critical for working with Arjuna as it is widely used across various other features like configuration, data driven testing etc.

```python
# arjuna-samples/arjex_core_features/tests/modules/test_02_value.py

from arjuna import *

@test
def test_value(my, request):
    v = Value("1")
    my.asserter.assertEqual(1, v.as_int())
    v = Value("1.1")
    my.asserter.assertEqual(1, v.as_int())

```

#### Points to Note
1. The test is coded as usual.
2. An object of Value is created by providing the object. Here were provide a string containing an integer.
3. `as_int` method of Value object is used for conversion of string to an int.
4. `my.asserter`'s `assertEqual` is used for equality assertion.
5. Same steps are repeated, but this time the string contains a float.
