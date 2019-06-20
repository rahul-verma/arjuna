from arjuna.client.core.connector import BaseSetuObject, SetuArg
from arjuna.client.core.action import *
from arjuna.client.core.config import ArjunaComponent


class GuiAutoComponentFactory:

    @staticmethod
    def Element(session, automator, setuId):
        return DefaultGuiElement(session, automator, setuId)

    @staticmethod
    def MultiElement(session, automator, setuId):
        return DefaultGuiMultiElement(session, automator, setuId)

    @staticmethod
    def DropDown(session, automator, setuId):
        return DefaultDropDown(session, automator, setuId)

    @staticmethod
    def RadioGroup(session, automator, setuId):
        return DefaultRadioGroup(session, automator, setuId)

    @staticmethod
    def Alert(session, automator, setuId):
        return DefaultAlert(session, automator, setuId)

    @staticmethod
    def MainWindow(session, automator, setuId):
        return DefaultMainWindow(session, automator, setuId)

    @staticmethod
    def DomRoot(session, automator):
        return DefaultDomRoot(session, automator)

    @staticmethod
    def Browser(session, automator):
        return DefaultBrowser(session, automator)


class BaseComponent(BaseSetuObject):

    def __init__(self, test_session, app_automator):
        super().__init__()
        self.__test_session = test_session
        self.__automator = app_automator

        if app_automator.is_gui():
            self._set_gui_setu_id_arg(app_automator.get_setu_id())
        else:
            self._set_automator_setu_id_arg(app_automator.get_setu_id())

        self._set_test_session_setu_id_arg(test_session.get_setu_id())

    def _get_automator(self):
        return self.__automator

    def _get_test_session(self):
        return self.__test_session


class BaseElement(BaseComponent):

    def __init__(self, test_session, app_automator, setu_id, index=None):
        super().__init__(test_session, app_automator)
        self._set_setu_id(setu_id)
        self._set_self_setu_id_arg("elementSetuId")

        if index is not None:
            self._add_args(
                SetuArg.arg("isInstanceAction", True),
                SetuArg.arg("instanceIndex", index)
            )


class DefaultGuiElement(BaseElement):

    def __init__(self, test_session, app_automator, setu_id, index=None):
        super().__init__(test_session, app_automator, setu_id, index)

    def enter_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_ENTER_TEXT, SetuArg.text_arg(text))

    def set_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_SET_TEXT, SetuArg.text_arg(text))

    def click(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_CLICK)

    def wait_until_clickable(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_WAIT_UNTIL_CLICKABLE)

    def check(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_CHECK)

    def uncheck(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ELEMENT_UNCHECK)


class DefaultGuiMultiElement(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def IndexedElement(self, index):
        return DefaultGuiElement(self._get_test_session(), self._get_automator(), self.get_setu_id(), index)


class DefaultDropDown(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def has_value_selected(self, value):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_VALUE_SELECTED, SetuArg.value_arg(value))
        return response.get_value_for_check_result()

    def has_index_selected(self, index):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_INDEX_SELECTED, SetuArg.index_arg(index))
        return response.get_value_for_check_result()

    def select_by_value(self, value):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_VALUE, SetuArg.value_arg(value))

    def select_by_index(self, index):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_INDEX, SetuArg.index_arg(index))

    def get_first_selected_option_value(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.get_value_for_value_attr()

    def get_first_selected_option_text(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT)
        return response.get_value_for_text()

    def has_visible_text_selected(self, text):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_VISIBLE_TEXT_SELECTED, SetuArg.text_arg(text))
        return response.get_value_for_check_result()

    def select_by_visible_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_VISIBLE_TEXT, SetuArg.text_arg(text))


class DefaultRadioGroup(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def has_value_selected(self, value):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.RADIOGROUP_HAS_VALUE_SELECTED, SetuArg.value_arg(value))
        return response.get_value_for_check_result()

    def has_index_selected(self, index):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.RADIOGROUP_HAS_INDEX_SELECTED, SetuArg.index_arg(index))
        return response.get_value_for_check_result()

    def select_by_value(self, value):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.RADIOGROUP_SELECT_BY_VALUE, SetuArg.value_arg(value))

    def select_by_index(self, index):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.RADIOGROUP_SELECT_BY_INDEX, SetuArg.index_arg(index))

    def get_first_selected_option_value(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.get_value_for_value_attr()


class DefaultAlert(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def confirm(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_CONFIRM)

    def dismiss(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_DISMISS)

    def get_text(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_GET_TEXT)
        return response.get_value_for_text()

    def send_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_SEND_TEXT, SetuArg.text_arg(text))


class DefaultBrowser(BaseComponent):

    def __init__(self, test_session, app_automator):
        super().__init__(test_session, app_automator)

    def go_to_url(self, url):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_TO_URL, SetuArg.arg("url", url))

    def go_back(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_BACK)

    def go_forward(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_FORWARD)

    def refresh(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_REFRESH)


class DefaultFrame(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)
        self._set_self_setu_id_arg("elementSetuId")

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.FRAME_FOCUS)

    def Frame(self, *withLocators):
        arg = [l.asMap() for l in withLocators]
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.FRAME_CREATE_FRAME, SetuArg.arg("locators", arg))
        return DefaultFrame(self._get_test_session(), self._get_automator(), response.get_value_for_element_setu_id())

    def ParentFrame(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.FRAME_GET_PARENT)
        return DefaultFrame(self._get_test_session(), self._get_automator(), response.get_value_for_element_setu_id())


class DefaultDomRoot(BaseComponent):

    def __init__(self, test_session, app_automator):
        super().__init__(test_session, app_automator)

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DOMROOT_FOCUS)

    def Frame(self, *with_locators):
        arg = [l.as_map() for l in with_locators]
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DOMROOT_CREATE_FRAME, SetuArg.arg("locators", arg))
        return DefaultFrame(self._get_test_session(), self._get_automator(), response.get_value_for_element_setu_id())

    def ParentFrame(self):
        raise Exception("DOM root does not have a parent frame.")


class AbstractBasicWindow(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def get_title(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.WINDOW_GET_TITLE)
        return response.get_value_for_key("title").as_string()

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.WINDOW_FOCUS)


class DefaultChildWindow(AbstractBasicWindow):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def close(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.CHILD_WINDOW_CLOSE)

    def MainWindow(self):
        return self._get_automator().MainWindow()


class DefaultMainWindow(AbstractBasicWindow):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def maximize(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_MAXIMIZE)

    def _take_element_finding_action(self, setu_action_type, *setu_args):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, setu_action_type, *setu_args)
        return response.get_value_for_element_setu_id()

    def ChildWindow(self, *withLocators):
        arg = [l.asMap() for l in withLocators]
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_CREATE_CHILD_WINDOW, SetuArg.arg("locators", arg))
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.get_value_for_element_setu_id())

    def LatestChildWindow(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_GET_LATEST_CHILD_WINDOW)
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.get_value_for_element_setu_id())

    def close_all_child_windows(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS)
