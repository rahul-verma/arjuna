# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def problem_in(*ids):
    '''
        Exclusion Relation: Problem based test function exclusion with exclude_if.

        Used to create a dependency of one test function on one or more other test functions.

        Arguments:
            *ids: One or more test function ids.

        Note:
            The depended-on test functions must belong to the same module as the dependent test function.
    '''
    if not ids:
        raise Exception("Atleast one test function id must be provided in problem_in call.")
    def call():
        return ids
    return call