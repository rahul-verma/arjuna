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

from arjuna import Page

from .widgets import *

class WPBasePage(Page):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.externalize()


class WPFullPage(WPBasePage):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.__top_nav = self.app.prepare_widget(TopNavBar(self))
        self.__left_nav = self.app.prepare_widget(LeftNavSideBar(self))

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav

