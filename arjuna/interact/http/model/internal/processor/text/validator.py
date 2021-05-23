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

import re
import abc
from arjuna.tpi.engine.asserter import AsserterMixIn
from arjuna.interact.http.model.internal.helper.yaml import convert_yaml_obj_to_content
from arjuna.tpi.parser.text import Text

class TextValidator(AsserterMixIn, metaclass=abc.ABCMeta):

    def __init__(self, response):
        super().__init__()
        self.__response = response

    @property
    def response(self):
        return self.__response

    @abc.abstractmethod
    def _eval_pattern_exists(self, pattern, exists):
        pass

    @abc.abstractmethod
    def _eval_pattern_match(self, pattern, actual, expected):
        pass

    def __extract_patterns(self, patterns):
        match_dict = {}
        patterns = type(patterns) in {set, tuple, list} and patterns or {str(patterns)}
        for pattern in patterns:
            try:
                match_dict[pattern] = self.response.find(pattern)
            except re.error as e:
                raise Exception("Wrong Regex syntax: >>{}<<. Error: {}".format(pattern, str(e)))
            except Exception:
                match_dict[pattern] = None
        return match_dict

    def assert_has_patterns(self, patterns):
        match_dict = self.__extract_patterns(patterns)
        match_dict = {k:v is not None for k,v in match_dict.items()}
        for regex, exists in match_dict.items():
            self._eval_pattern_exists(regex, exists)

    def assert_match_for_patterns(self, patterns):
        match_dict = self.__extract_patterns([k for k in patterns.keys()])
        for regex, actual in match_dict.items():
            self._eval_pattern_match(regex, actual, patterns[regex])

class ExpectedTextValidator(TextValidator):

    def __init__(self, response):
        super().__init__(response)

    def _eval_pattern_exists(self, pattern, exists):
        self.asserter.assert_true(exists, f"Expected pattern >>{pattern}<< was not found.")

    def _eval_pattern_match(self, pattern, actual, expected):
        self.asserter.assert_equal(actual, expected, f"Value for pattern >>{pattern}<< does not match.")

class UnexpectedTextValidator(TextValidator):

    def __init__(self, response):
        super().__init__(response)

    def _eval_pattern_exists(self, pattern, exists):
        self.asserter.assert_false(exists, f"Unexpected pattern >>{pattern}<< was found.")

    def _eval_pattern_match(self, pattern, actual, expected):
        self.asserter.assert_equal(actual, expected, f"Value for pattern >>{pattern}<< does not match.")


