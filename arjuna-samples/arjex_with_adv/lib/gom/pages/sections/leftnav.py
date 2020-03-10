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

from enum import Enum, auto
from arjuna import *
from .base import WPBaseSection

class LeftNav(WPBaseSection):

    class labels(Enum):
        settings = auto()

    def __init__(self, page):
        super().__init__(page, With.id("adminmenu"))

    def validate_readiness(self):
        self.element(self.labels.settings)

    @property
    def settings(self):
        from arjex_with_adv.lib.gom.pages.settings import Settings
        self.element(self.labels.settings).click()
        return Settings(self)
