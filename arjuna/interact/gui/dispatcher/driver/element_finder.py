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

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from arjuna.tpi.error import *
from arjuna.core.error import *

class ElementFinder:
    BY_MAP = {
        "ID": By.ID,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "CLASS_NAME": By.CLASS_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "XPATH": By.XPATH
    }
    
    @classmethod
    def find_element(cls, container, byType, byValue):
        from arjuna import log_debug
        log_debug(f"Finding element in container:{container} with wtype:{byType} and wvalue:{byValue}")
        try:
            return container.find_element(cls.BY_MAP[byType.upper()], byValue)
        except Exception as e:
            raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue))


    @classmethod
    def find_elements(cls, container, byType, byValue):
        elements = container.find_elements(cls.BY_MAP[byType.upper()], byValue)
        if len(elements) == 0:
            raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue))
        return elements
