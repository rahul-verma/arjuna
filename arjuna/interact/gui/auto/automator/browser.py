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

from arjuna.core.enums import ArjunaOption

class Browser:

    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def go_to_url(self, url):
        self.automator.dispatcher.go_to_url(url=url)

    def go_back(self, url):
        self.automator.dispatcher.go_back()

    def go_forward(self, url):
        self.automator.dispatcher.go_forward()

    def refresh(self, url):
        self.automator.dispatcher.refresh()

    def execute_javascript(self, js, *args):
        return self.automator.dispatcher.execute_javascript(js, *args)