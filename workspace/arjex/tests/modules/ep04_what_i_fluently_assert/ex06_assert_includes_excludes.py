'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *


'''
Explore more situations for this.
'''


@test_function
def assert_contains_single_value(my):
    validator = my.steps.validate("Higher purpose")

    # List containing a value
    validator.assert_that([1,2,3]).includes(2)
    validator.assert_that([1, 2, 3]).excludes(4)

    # Tuple containing a value
    validator.assert_that((1,2,3)).includes(2)
    validator.assert_that((1,2,3)).excludes(4)

    # Set containing a value
    validator.assert_that({1,2,3}).includes(2)
    validator.assert_that({1,2,3}).excludes(4)

    # Dictionary containing a key
    validator.assert_that({1:'a', 2:'b', 3:'c'}).includes(2)
    validator.assert_that({1:'a', 2:'b', 3:'c'}).excludes(4)

    # Dictionary containing key and value pair
    validator.assert_that({1:'a', 2:'b', 3:'c'}).includes({2:'b'})
    validator.assert_that({1:'a', 2:'b', 3:'c'}).excludes({4: 'd'})
    validator.assert_that({1:'a', 2:'b', 3:'c'}).excludes({3: 'e'})


@test_function
def assert_contains_multi_values(my):
    validator = my.steps.validate("Higher purpose")

    # Any iterable works. The container can be a list, tuple, set or dictionary
    # The expected values can be passed as a list, tuple, set as well.
    # The expected values can be passed as a dictionary only if the actual container is of type dictionary
    # Here we consider the container as list and play with container for expected values

    validator.assert_that([1, 2, 3]).includes([1,2])
    validator.assert_that([1, 2, 3]).includes((1,2))
    validator.assert_that([1, 2, 3]).includes({1,2})

    # This would throw exception.
    #validator.assert_that([1, 2, 3]).includes({1:'a', 2:'c'})

    # This works
    validator.assert_that({1:'a', 2:'b', 3:'c'}).includes({1:'a', 3:'c'})