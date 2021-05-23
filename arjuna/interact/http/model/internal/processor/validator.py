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

from arjuna.tpi.engine.asserter import AsserterMixIn
from arjuna.tpi.helper.arjtype import NotFound
from arjuna.tpi.parser.text import Text

class Validator(AsserterMixIn):

    def __init__(self, response):
        super().__init__()
        self.__response = response

    @property
    def response(self):
        return self.__response

    def validate(self, name, target):
        stored_value = self.__response.store[name]

        def validate_found(expected_to_be_found):
            exists = True
            if isinstance(stored_value, NotFound):
                exists = False
            if expected_to_be_found:
                self.asserter.assert_true(exists, f"No value was extracted for name >>{name}<<.")
            else:
                self.asserter.assert_false(exists, ">>{}<< was extracted for name >>{}<<. It should not exist.".format(stored_value, name))

        if "exists" not in target:
            validate_found(True)
        else:
            validate_found(target['exists'])
            # No further validations as it is not found
            if not target['exists']:
                return

        for k,v in target.items():
            k = k.lower()
            if k == "exists":
                continue
            elif k == "contains":
                proc_stored_value = stored_value
                if type(stored_value) is str:
                    proc_stored_value = Text(stored_value)
                for item in v:
                    getattr(proc_stored_value, "assert_contains")(item, msg=f"Extracted value for >>{name}<< does not contain >>{item}<<.")
            elif k == "min":
                self.asserter.assert_min(stored_value, v, msg=f"Extracted value for >>{name}<< did not match min value criterion.")





    