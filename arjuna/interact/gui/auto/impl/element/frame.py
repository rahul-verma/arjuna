import os

from arjuna.tpi import Arjuna
from arjuna.interact.gui.auto.impl.element.guielement import GuiElement
from arjuna.interact.gui.auto.impl.locator.emd import SimpleGuiElementMetaData
from arjuna.interact.gui.auto.impl.source.parser import FrameSource

class FrameContainer:
    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def __check_tag(self, wrapped_element):
        tag = wrapped_element.get_source(refind=False).get_tag_name()
        if tag.lower() != "iframe":
            raise Exception("The element should have a 'iframe' tag for IFrame element. Found: " + tag)

    def define_frame(self, locator_meta_data):
        found = False
        frame = None
        for locator in locator_meta_data.locators: 
            try:
                if locator.ltype.name == "INDEX":
                    index = locator.lvalue
                    emd = SimpleGuiElementMetaData("xpath", "//iframe")
                    multi_element = self.automator.define_multielement(emd)
                    multi_element.find()
                    wrapped_element = multi_element.get_instance_at_index(index)
                    self.__check_tag(wrapped_element)
                    frame = IPartialFrame(self.automator, self, multi_element, wrapped_element)
                else:
                    emd = SimpleGuiElementMetaData(locator.ltype.name, locator.lvalue)
                    wrapped_element = self.automator.define_element(emd)
                    wrapped_element.find()
                    self.__check_tag(wrapped_element)
                    frame = IFrame(self.automator, self, wrapped_element)

                found = True
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(e)
                continue

        if not found:
            raise Exception("Could not locate frame with locator(s): {}".format([str(l) for l in locator_meta_data.locators]))

        return frame

    def enumerate_frames(self):
        self.focus()
        emd = SimpleGuiElementMetaData("xpath", "//iframe")
        multi_element = self.automator.create_multielement(emd)
        ret_str = os.linesep.join(["--> " + s for s in multi_element.get_source()._get_root_content_as_list()])
        return self._source_parser.get_root_content() + os.linesep + ret_str

class DomRoot(FrameContainer):

    def __init__(self, automator):
        super().__init__(automator)
        self.__frame_context = "root"
        self._source_parser = self.automator.get_source()

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
        self.automator.dispatcher.focus_on_dom_root()
        self.set_frame_context_as_root() 

    def get_source(self):
        self.focus()
        return self.automator.get_source()

class IFrame(FrameContainer):

    def __init__(self, automator, dom_root, wrapped_element):
        super().__init__(automator)
        self.__dom_root = dom_root
        self.__parent_frames = []
        self.__wrapped_element = wrapped_element
        self._source_parser = FrameSource(self)

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
        self.wrapped_element.find()
        self._source_parser.set_root_source(self.wrapped_element.get_source(refind=False).get_root_content())
        self.automator.dispatcher.focus_on_frame(self.wrapped_element.dispatcher)
        self.dom_root.set_frame_context(self)

    def _get_html_content_from_remote(self):
        return self.automator.get_source()

    def get_wrapped_element(self):
        return self.wrapped_element

    def get_source(self):
        self._source_parser.load()
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

    def __init__(self, automator, dom_root, melement, wrapped_element):
        super().__init__(automator, dom_root, wrapped_element)
        self.__melement = melement

    def focus(self):
        self.__melement.find()
        self.automator.dispatcher.focus_on_frame(self.wrapped_element.dispatcher)
        self.dom_root.set_frame_context(self)