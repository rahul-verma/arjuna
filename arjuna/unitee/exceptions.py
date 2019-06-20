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

from arjuna.lib.exceptions import *

class DataSourceFinished(StopIteration):
    def __init__(self, msg=None):
        super().__init__(msg is None and "Done" or msg)


class EmptyListDataRecordLookupException(Exception):
    def __init__(self, index):
        super().__init__("Invalid index [%s] used for list data record lookup. It is empty.".format(index))


class ListDataRecordLookupException(Exception):
    def __init__(self, index, max_index):
        super().__init__(
            "Invalid index [%s] used for list data record lookup. Use indices between 0 and %d".format(index,
                                                                                                       max_index))


class MapDataRecordLookupException(Exception):
    def __init__(self, key):
        super().__init__("Invalid Key/header [%s] used for map data record lookup.".format(key))


class DataSourceConstructionError(Exception):
    def __init__(self, message, name, exc):
        super().__init__(message)
        self.name = name
        self.exc = exc

    def get_Exception(self):
        return self.exc

    def get_Name(self):
        return self.name


class InvalidTestObjectException(Exception):
    pass


class SessionNodesFinishedException(Exception):
    def __init__(self):
        super().__init__("Done")


class SubTestsFinished(Exception):
    def __init__(self):
        super().__init__("Done")


class TestGroupsFinishedException(Exception):
    def __init__(self):
        super().__init__("Done")


class PickerMisConfigurationException(Exception):
    def __init__(self):
        super().__init__("Picker is misconfigured.")

# Test Result Related

class StepResultEvent(ArjunaException):
    def __init__(self, step):
        super().__init__(step.assert_message)
        self.step = step

class Pass(StepResultEvent):
    def __init__(self, check):
        super().__init__(check)


class Error(StepResultEvent):
    def __init__(self, step):
        super().__init__(step)


class Failure(StepResultEvent):
    def __init__(self, step):
        super().__init__(step)

class DependencyNotMet(Exception):
    def __init__(self, iid):
        self.iid = iid