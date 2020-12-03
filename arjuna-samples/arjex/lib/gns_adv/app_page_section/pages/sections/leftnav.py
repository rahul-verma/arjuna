# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from enum import Enum, auto
from arjuna import *
from .base import WPBaseGuiSection

class LeftNav(WPBaseGuiSection):
    
    def __init__(self, page):
        super().__init__(page, label="LeftNav", root=None)

    @property
    def settings_page(self):
        from arjex.lib.gns_adv.app_page_section.pages.settings import Settings
        self.gns.settings.click()
        return Settings(self)

    @property
    def pages_page(self):
        from arjex.lib.gns_adv.app_page_section.pages.pages import Pages
        self.gns.pages.click()
        return Pages(self)


class LeftNavCodedRootLabel(WPBaseGuiSection):
    
    def __init__(self, page):
        super().__init__(page, label="LeftNav", root="menu")

    @property
    def settings_page(self):
        from arjex.lib.gns_adv.app_page_section.pages.settings import Settings
        self.gns.settings.click()
        return Settings(self)


class LeftNavCodedRootLocator(WPBaseGuiSection):
    
    def __init__(self, page):
        super().__init__(page, label="LeftNav", root=GuiWidgetDefinition(id="adminmenu"))

    @property
    def settings_page(self):
        from arjex.lib.gns_adv.app_page_section.pages.settings import Settings
        self.gns.settings.click()
        return Settings(self)
