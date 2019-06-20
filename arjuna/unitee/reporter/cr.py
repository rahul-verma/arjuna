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

import threading
from collections import OrderedDict
from arjuna.tpi import Arjuna
from arjuna.lib.thread.decorators import *
from arjuna.unitee.reporter.result.types import SteppedResult

class ConsoleReporter:

    def __init__(self):
        self.lock = threading.RLock()
        self.console = Arjuna.get_console()

    @sync_method('lock')
    def __print(self, heading, rdict={}):
        self.console.marker(25)
        self.console.display(heading)
        self.console.marker(25)
        for k,v in rdict.items():
            if v != "-":
                self.console.display_multiline_key_value(k,v)

    def update_info(self, rdict):
        self.__print("Information Notification", rdict)

    def update_issue(self, issue):
        self.__print("Issue Notification", issue)

    def update_test_object_result(self, reportable):
        if reportable.has_steps():
            rdict = OrderedDict(reportable.result)
            for step in reportable.steps:
                rdict.update(step)
                rdict['evars'] = "-"
                rdict['data_record'] = "-"
                rdict['rcode'] = "-"
                rdict['props'] = "-"
                rdict['user_props'] = "-"
                rdict['tags'] = "-"
                self.__print("Step Notification", rdict)

        self.__print("Result Notification", reportable.result)

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def update_info_headers(self, headers):
        pass

    def update_execution_headers(self, headers):
        pass

    def update_step_headers(self, headers):
        pass

    def update_issue_headers(self, headers):
        pass