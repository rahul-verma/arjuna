from arjuna.setu.types import SetuManagedObject
from arjuna.setuext.guiauto.impl.element.guielement import GuiElement
from arjuna.setuext.guiauto.impl.locator.emd import SimpleGuiElementMetaData

from arjuna.setu import Setu

class FrameContainer(SetuManagedObject):
    def __init__(self, automator):
        super().__init__()
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def _act(self, json_dict):
        return self.__automator.actor_callable(json_dict)

    def __check_tag(self, wrapped_element):
        tag = wrapped_element.get_tag_name()
        if tag.lower() != "iframe":
            raise Exception("The element should have a 'iframe' tag for IFrame element. Found: " + tag)

    def create_frame(self, locator_meta_data):
        found = False
        frame = None
        for locator in locator_meta_data.locators: 
            try:
                if locator.ltype.name == "INDEX":
                    index = locator.lvalue
                    emd = SimpleGuiElementMetaData("xpath", "//iframe")
                    multi_element = self.automator.create_multielement(emd)
                    multi_element.find()
                    wrapped_element = multi_element.get_instance_at_index(index)
                    self.__check_tag(wrapped_element)
                    frame = IPartialFrame(self.automator, self, multi_element, wrapped_element)
                else:
                    emd = SimpleGuiElementMetaData(locator.ltype.name, locator.lvalue)
                    wrapped_element = self.automator.create_element(emd)
                    self.__check_tag(wrapped_element)
                    frame = IFrame(self.automator, self, wrapped_element)

                found = True
            except Exception as e:
                print(e)
                continue

        if not found:
            raise Exception("Could not locate frame with locator(s): {}".format(locator_meta_data.locators))
        else:
            self.automator.add_frame(frame)
            return frame

class DomRoot(FrameContainer):

    def __init__(self, automator):
        super().__init__(automator)
        self.__frame_context = "root"
        self.automator.add_frame(self)

    @property
    def frame_context(self):
        return self.__frame_context

    def __set_frame_context_str(self, name):
        self.__frame_context = name
        Setu.get_logger().debug("Automator is in {} frame".format(self.__frame_context))

    def set_frame_context(self, frame):
        self.__set_frame_context_str(frame.get_setu_id())

    def set_frame_context_as_root(self):
        self.__set_frame_context_str("root")  

    def focus(self):
        self.automator.dispatcher.focus_on_dom_root()
        self.set_frame_context_as_root() 

# UUID is for client reference. Agent does not know about this.
class IFrame(FrameContainer):

    def __init__(self, automator, dom_root, wrapped_element):
        super().__init__(automator)
        self.__dom_root = dom_root
        self.__parent_frames = []
        self.__wrapped_element = wrapped_element

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

    def focus(self):
        self.wrapped_element.find()
        self.automator.dispatcher.focus_on_frame(self.wrapped_element.setu_id)
        self.dom_root.set_frame_context(self)

    # def focus_on_parent(self):
    #     self._act(TestAutomatorActionBodyCreator.jump_to_parent_frame())
    #     if self.__parent_frames:
    #         self.dom_root.set_frame_context(self.__parent_frames[-1])
    #     else:
    #         self.dom_root.set_frame_context_as_root()

    def get_parent(self):
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
        self.automator.dispatcher.focus_on_frame(self.__melement.setu_id, True, self.wrapped_element._get_instance_number())
        self.dom_root.set_frame_context(self)