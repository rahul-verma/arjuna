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

import abc
from arjuna.core.error import WaitableError, _GuiWidgetPresentError
from arjuna.tpi.error import GuiWidgetNotFoundError
from arjuna import track

@track("debug")
class ElementFinder:
    def __init__(self, container): #, obj_name=""):
        self.__container = container
        self.__config = container.config
        # self.__obj_name = obj_name

    @property
    def config(self):
        return self.__config

    @property
    def container(self):
        return self.__container

    @abc.abstractmethod
    def _create_element_flat_or_nested(self, wmd):
        pass

    @abc.abstractmethod
    def _create_multielement_flat_or_nested(self, wmd):
        pass

    def check_for_absence(self, dispatcher_call, wmd, context="ELEMENT"):
        try:
            self.find(dispatcher_call, wmd, context)
        except GuiWidgetNotFoundError as e:
            # This is expected
            pass
        else:
            raise _GuiWidgetPresentError(*wmd.locators)

    def find(self, dispatcher_call, wmd, context="ELEMENT"):
        from arjuna import log_trace, log_debug
        log_trace("Finding with wmd: {}".format(str(wmd)))
        from arjuna import Arjuna
        found = False
        js_call_name = context == "ELEMENT" and "_find_element_with_js" or "_find_multielement_with_js"
        js_call = getattr(self.container, js_call_name)
        locators = wmd.locators
        if context != "ELEMENT":
            if "POINT" in {l.ltype.name for l in locators}:
                raise ConditionException("With.POINT can be used only with GuiElement.")

        # Prepare Relations dict

        we = None
        for locator in locators:
            try:
                if locator.ltype.name == "POINT":
                    # Assumption here is that this container is automator.
                    size, dispatcher = js_call(locator.lvalue)
                elif locator.ltype.name == "JS":
                    size, dispatcher = js_call(locator.lvalue)
                else:
                    lvalue = locator.lvalue
                    if locator.ltype.name == "XPATH":
                        if not lvalue.startswith("."):
                            lvalue = "." + lvalue
                    log_debug("Trying out locator {} with value {}".format(locator.ltype.name, lvalue))
                    size, dispatcher = dispatcher_call(locator.ltype.name, lvalue, relations=wmd.meta.relations, filters=wmd.meta.filters)
                return locator.ltype.name, locator.lvalue, size, dispatcher
            except WaitableError as e:
                log_debug("Waitable exception raised.")
                we = e
            except Exception as f:
                log_debug("Non-Waitable exception raised: {}: {}".format(f.__class__.__name__, str(f)))
                raise f
            else:
                we = None
        if not found:
            raise GuiWidgetNotFoundError(*wmd.locators, relations=wmd.meta.relations, filters=wmd.meta.filters, container=self.__container)