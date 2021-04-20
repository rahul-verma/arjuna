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

import time
import traceback

from arjuna.tpi.error import *
from arjuna.core.error import *

# This code is inspired by fluent wait concept in Selenium Webdriver
# Reference code: https://github.com/browserstack/selenium-webdriver-python/edit/master/selenium/webdriver/support/wait.py
# However, rather than a Selnium WebDriver specific and driver level concept,
# Setu aims to make it a more generic concept available beyond WebDriver and GUI automation.
# Setu makes waiting accessible through a condition rather than the other way round.
# i.e. object.condition(args).wait(), rather than wait(driver).condition(args)

class ConditionException(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class Condition:

    def __init__(self, dynamic_caller, *args, **kwargs):
        self.__dynamic_caller = dynamic_caller
        self.__args = args
        self.__kwargs = kwargs
        self.__call_result = None

    def get_call_result(self):
        return self.__call_result

    def wait(self, *, max_wait=60, poll_interval=0.5):
        from arjuna import log_debug
        log_debug("Dynamic wait call triggered with max_wait: {}".format(max_wait))
        end_time = time.time() + max_wait
        e = None
        etrace = None
        while(True):
            try:
                if self.is_met():
                    return self.get_call_result()
            except ConditionException as ce:
                raise ce
            except WaitableError as we:
                e = we
                import traceback
                etrace = traceback.format_exc()
                pass
            except Exception as f:
                import traceback
                raise Exception("An unexpected exception occured in dynamic wait. Message: {}. Trace: {}".format(str(f), traceback.format_exc()))
            time.sleep(poll_interval)
            ctime = time.time()
            if(ctime > end_time):
                break
        raise ArjunaTimeoutError(self.__class__.__name__, str(e) + etrace)

    def execute(self):
        try:
            self.__call_result = self.__dynamic_caller.call(*self.__args, **self.__kwargs)
        except ArjunaTimeoutError as e:
            raise ArjunaTimeoutError("ArjunaTimeOut: {}".format(str(e)))

class CommandCondition(Condition):

    def __init__(self, dynamic_caller, returns_none=True):
        super().__init__(dynamic_caller)
        self.__returns_none = returns_none

    def is_met(self):
        self.execute()
        if self.__returns_none: return True
        return self.get_call_result() is not None

class BooleanCondition(Condition):

    def __init__(self, dynamic_caller, expectation_type=True):
        super().__init__(dynamic_caller)
        self.__expectation_type = expectation_type

    def is_met(self):
        try:
            self.execute()
            return self.__expectation_type == self.get_call_result()
        except Exception as e:
            raise ConditionException("Unexpected exception in boolean condition checking: " + str(e) + traceback.format_exc())