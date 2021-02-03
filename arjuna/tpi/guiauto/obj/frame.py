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

import os

from arjuna import Arjuna
from arjuna.interact.gui.auto.finder.wmd import SimpleGuiWidgetMetaData
from arjuna.tpi.guiauto.source.frame import _GuiFrameSource

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.core.error import ChildWindowNotFoundError

class FrameConditions:

    def __init__(self, frame):
        self.__frame = frame

    @property
    def frame(self):
        return self.__frame

    def FrameIsPresent(self, wmd, *args, **kwargs):
        caller = DynamicCaller(self.frame._find_frame, wmd, *args, **kwargs)
        return CommandCondition(caller)

class FrameContainer:

    def __init__(self, gui):
        self.__gui = gui
        self.__automator = gui._automator
        self.__conditions = FrameConditions(self)

    @property
    def max_wait(self):
        return self.__automator.config.guiauto_max_wait

    def __check_tag(self, wrapped_element):
        tag = wrapped_element.source.tag
        if tag.lower() != "iframe":
            raise Exception("The element should have a 'iframe' tag for IFrame element. Found: " + tag)

    def frame(self, wmd):
        return self.__conditions.FrameIsPresent(wmd).wait(max_wait=self.max_wait)

    def _find_frame(self, wmd):
        found = False
        frame = None
        for locator in wmd.locators: 
            try:
                if locator.ltype.name == "INDEX":
                    index = locator.lvalue
                    wmd = SimpleGuiWidgetMetaData("xpath", "//iframe")
                    multi_element = self.__automator.multi_element(self.gui, wmd)
                    # multi_element.find()
                    try:
                        wrapped_element = multi_element[index]
                    except:
                        # In case another identifier is present it should be tried.
                        continue
                    self.__check_tag(wrapped_element)
                    frame = IPartialFrame(self.gui, self, multi_element, wrapped_element)
                else:
                    wmd = SimpleGuiWidgetMetaData(locator.ltype.name, locator.lvalue)
                    wrapped_element = self.__automator.element(self.gui, wmd)
                    # wrapped_element.find()
                    self.__check_tag(wrapped_element)
                    frame = IFrame(self.gui, self, wrapped_element)

                return frame
            except WaitableError as f:
                continue  
            except Exception as e:
                raise Exception(str(e) + traceback.format_exc()) 

        raise ChildFrameNotFoundError(*wmd.locators)

    def enumerate_frames(self):
        self.focus()
        wmd = SimpleGuiWidgetMetaData("xpath", "//iframe")
        multi_element = self.__automator.create_multielement(wmd)
        ret_str = os.linesep.join(["--> " + s for s in multi_element.source._get_root_content_as_list()])
        return self._source_parser.get_root_content() + os.linesep + ret_str

class DomRoot(FrameContainer):

    def __init__(self, gui):
        super().__init__(gui)
        self.__frame_context = "root"
        self._source_parser = self.__automator.source

    @property
    def frame_context(self):
        return self.__frame_context

    def __set_frame_context_str(self, name):
        self.__frame_context = name
        Arjuna.get_logger().debug("Automator is in {} frame".format(self.__frame_context))
        print("Automator is in {} frame".format(self.__frame_context))

    def set_frame_context(self, frame):
        self.__set_frame_context_str(frame)

    def set_frame_context_as_root(self):
        self.__set_frame_context_str("root")  

    def is_in_root_context(self):
        return self.__frame_context == "root"

    def focus(self):
        self.__automator.dispatcher.focus_on_dom_root()
        self.set_frame_context_as_root() 

    @property
    def source(self):
        self.focus()
        return self.__automator.source

class IFrame(FrameContainer):

    def __init__(self, gui, dom_root, wrapped_element):
        super().__init__(gui)
        self.__dom_root = dom_root
        self.__parent_frames = []
        self.__wrapped_element = wrapped_element
        self._source_parser = _GuiFrameSource(self)

    @property
    def dom_root(self):
        return self.__dom_root

    @property
    def wrapped_element(self):
        return self.__wrapped_element

    def set_parents(self, parents):
        self.__parent_frames = parents

    def _act(self, json_dict):
        return self.dom_root._act(json_dict)

    def _focus_on_parents(self):
        if self.__parent_frames:
            for parent in self.__parent_frames:
                parent.focus()

    def __reload_wrapped_element(self):
        self.wrapped_element.find()

    def focus(self):
        if not self.dom_root.is_in_root_context():
            self.dom_root.focus()
            self._focus_on_parents()
        # self.wrapped_element.find()
        self._source_parser.set_root_source(self.wrapped_element.source.content.root)
        self.__automator.dispatcher.focus_on_frame(self.wrapped_element.dispatcher)
        self.dom_root.set_frame_context(self)

    def _get_html_content_from_remote(self):
        return self.__automator.source

    def get_wrapped_element(self):
        return self.wrapped_element

    @property
    def source(self) -> _GuiFrameSource:
        self._source_parser._load()
        return self._source_parser

    # def focus_on_parent(self):
    #     self._act(TestAutomatorActionBodyCreator.jump_to_parent_frame())
    #     if self.__parent_frames:
    #         self.dom_root.set_frame_context(self.__parent_frames[-1])
    #     else:
    #         self.dom_root.set_frame_context_as_root()

    @property
    def parent(self):
        if self.__parent_frames:
            return self.__parent_frames[-1]
        else:
            return self.dom_root


class IPartialFrame(IFrame):

    def __init__(self, gui, dom_root, melement, wrapped_element):
        super().__init__(gui, dom_root, wrapped_element)
        self.__melement = melement

    def focus(self):
        # self.__melement.find()
        self.__automator.dispatcher.focus_on_frame(self.wrapped_element.dispatcher)
        self.dom_root.set_frame_context(self)