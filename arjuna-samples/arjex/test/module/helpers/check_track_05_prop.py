'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

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

from arjuna import *

class Sample:

    def __init__(self):
        self._p = None

    @track
    @property
    def prop1(self):
        log_debug("prop1 getter")
        return self._p

    @track
    @prop1.setter
    def prop1(self, value):
        log_debug("prop1 setter")
        self._p = value

    @track("info")
    @property
    def prop2(self):
        log_debug("prop2 getter")
        return self._p

    @track("info")
    @prop2.setter
    def prop2(self, value):
        log_debug("prop2 setter")
        self._p = value

    @track("info")
    @property
    def prop3(self):
        log_debug("prop3 getter")
        return self._p

    @property
    def prop4(self):
        log_debug("prop4 getter")
        return self._p

    @track("info")
    @prop4.setter
    def prop4(self, value):
        log_debug("prop4 setter")
        self._p = value

@test
def check_tracking_prop(request):
    s = Sample()
    print(s.prop1)
    s.prop1 = 3
    s.prop1

    s.prop2
    s.prop2 = 3
    s.prop2

    s.prop3

    s.prop4
    s.prop4 = 3
    s.prop4
