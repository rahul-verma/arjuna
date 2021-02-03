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

import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from arjuna.tpi.error import *
from arjuna.core.error import *
from selenium.webdriver.support.relative_locator import RelativeBy
from selenium.webdriver.remote.webelement import WebElement
from arjuna.tpi.tracker import track

@track("debug")
class SeleniumElementFinder:
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

    RELATION_MAP = {
        "above": "above",
        "below": "below",
        "right_of": "to_right_of",
        "left_of": "to_left_of",
        "near": "near",
    }
    
    @classmethod
    def __create_relative_by(cls, byType, byValue, relations):
        from arjuna import log_debug
        relative_by = RelativeBy({byType: byValue})
        for k,v in relations.items():
            try:
                getattr(relative_by, cls.RELATION_MAP[k.lower()])(v)
            except:
                pass
        log_debug("Root" + str(relative_by.root))
        log_debug("Filters" + str(relative_by.filters))
        return relative_by
        
    # @classmethod
    # def find_element(cls, container, byType, byValue, *, relations=None):
    #     from arjuna import log_debug
    #     log_debug(f"Finding element in container:{container} with wtype:{byType} and wvalue:{byValue} with relations: {relations}")
    #     try:
    #         byType = cls.BY_MAP[byType.upper()]
    #         if not relations:
    #             return container.find_element(byType, byValue)
    #         else:
    #             # Currently Selenium supports Relative locator only for find_elements and at driver level
    #             # For nested element finding change to WebDriver instance if relations are defined.
    #             if isinstance(container, WebElement):
    #                 container = container.parent
    #             elements = container.find_elements(cls.__create_relative_by(byType, byValue, relations))
    #             if len(elements) == 0:
    #                 raise Exception("No elements found.")
    #             else:
    #                 return elements[0]
    #     except Exception as e:
    #         raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue))

    _POS = {
        "first" : 1,
        "last" : -1
    }

    @classmethod
    def find_element(cls, container, byType, byValue, *, relations=None, filters=None):
        from arjuna import log_debug
        log_debug(f"Finding element in container:{container} with wtype:{byType} and wvalue:{byValue} with relations: {relations} and filters: {filters}")
        elements = cls.find_elements(container, byType, byValue, relations=relations, filters=filters)
        return elements[0]

    @classmethod
    def find_elements(cls, container, byType, byValue, *, relations=None, filters=None):
        from arjuna import log_debug
        log_debug(f"Finding elements in container:{container} with wtype:{byType} and wvalue:{byValue} with relations: {relations} and filters: {filters}")
        sbyType = cls.BY_MAP[byType.upper()]
        if not relations:
            elements = container.find_elements(sbyType, byValue)
        else:
            # Currently Selenium supports Relative locator only for find_elements and at driver level
            # For nested element finding change to WebDriver instance if relations are defined.
            if isinstance(container, WebElement):
                container = container.parent
            rby = cls.__create_relative_by(sbyType, byValue, relations)
            log_debug("Selenium find_elements call made with RelativeBy: {}".format(rby.to_dict()))
            elements = container.find_elements(rby)         
        if len(elements) == 0:
            raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue), message="No element found for Selenium locator")   
        if filters is not None:
            if "pos" in filters:
                log_debug("Filtering elements with filter: {}".format(filters["pos"]))
                try:
                    extracted_elements = filters["pos"].extract(elements)
                    if type(extracted_elements) is not list:
                        return [extracted_elements]
                    else:
                        return extracted_elements
                except Exception as e:
                    log_debug("Exception in filters processing: {}".format(e))
                    raise GuiWidgetNotFoundError("By.{}={}".format(byType, byValue), message="No element found for Selenium locator after applying position filters.")   
        return elements
