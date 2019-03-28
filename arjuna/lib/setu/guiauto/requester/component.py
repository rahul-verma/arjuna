from arjuna.lib.setu.core.requester.connector import BaseSetuObject, SetuArg
from arjuna.lib.setu.core.requester.config import SetuActionType


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
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_ENTER_TEXTs)

    def set_text(self, text):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_ENTER_TEXT)

    def click(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_CLICK)

    def wait_until_clickable(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_WAIT_UNTIL_CLICKABLE)

    def check(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_CHECK)

    def uncheck(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_UNCHECK)


class DefaultGuiMultiElement(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def get_instance_at_index(self, index):
        return GuiAutoComponentFactory.GuiElement(self._get_test_session(), self._get_automator(), self.getSetuId(), index)


class DefaultDropDown(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def has_value_selected(self, value):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_VALUE_SELECTED, SetuArg.valueArg(value))
        return response.getValueForCheckResult()

    def has_index_selected(self, index):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_INDEX_SELECTED, SetuArg.indexArg(index))
        return response.getValueForCheckResult()

    def select_by_value(self, value):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VALUE, SetuArg.valueArg(value))

    def select_by_index(self, index):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_INDEX, SetuArg.indexArg(index))

    def get_first_elected_option_value(self):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.getValueForValueAttr()

    def get_first_selected_option_text(self):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT)
        return response.getValueForText()

    def has_visible_text_selected(self, text):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_VISIBLE_TEXT_SELECTED, SetuArg.textArg(text))
        return response.getValueForCheckResult()

    def select_by_visible_text(self, text):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VISIBLE_TEXT, SetuArg.textArg(text))


class DefaultRadioGroup(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def has_value_selected(self, value):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_HAS_VALUE_SELECTED, SetuArg.valueArg(value))
        return response.getValueForCheckResult()

    def has_index_selected(self, index):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_HAS_INDEX_SELECTED, SetuArg.indexArg(index))
        return response.getValueForCheckResult()

    def select_by_value(self, value):
        self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_VALUE, SetuArg.valueArg(value))

    def select_by_index(self, index):
        self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_INDEX, SetuArg.indexArg(index))

    def get_first_selected_option_value(self):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.getValueForValueAttr()


class DefaultAlert(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def confirm(self):
        self._send_request(SetuActionType.GUIAUTO_ALERT_CONFIRM)

    def dismiss(self):
        self._send_request(SetuActionType.GUIAUTO_ALERT_DISMISS)

    def get_text(self):
        response = self._send_request(SetuActionType.GUIAUTO_ALERT_GET_TEXT)
        return response.getValueForText()

    def send_text(self, text):
        self._send_request(SetuActionType.GUIAUTO_ALERT_SEND_TEXT, SetuArg.textArg(text))


class DefaultBrowser(BaseComponent):

    def __init__(self, test_session, app_automator):
        super().__init__(test_session, app_automator)

    def go_to_url(self, url):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_TO_URL, SetuArg.arg("url", url))

    def go_back(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_BACK)

    def go_forward(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_FORWARD)

    def refresh(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_REFRESH)


class DefaultFrame(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)
        self._set_self_setu_id_arg("elementSetuId")

    def focus(self):
        self._send_request(SetuActionType.GUIAUTO_FRAME_FOCUS)

    def Frame(self, *withLocators):
        arg = [l.asMap() for l in withLocators]
        response = self._send_request(SetuActionType.GUIAUTO_FRAME_CREATE_FRAME, SetuArg.arg("locators", arg))
        return GuiAutoComponentFactory.Frame(self._get_test_session(), self._get_automator(), response.getValueForElementSetuId())

    def Parent(self):
        response = self._send_request(SetuActionType.GUIAUTO_FRAME_GET_PARENT)
        return GuiAutoComponentFactory.Frame(self._get_test_session(), self._get_automator(), response.getValueForElementSetuId())


class DefaultDomRoot(BaseComponent):

    def __init__(self, test_session, app_automator):
        super().__init__(test_session, app_automator)

    def focus(self):
        self._send_request(SetuActionType.GUIAUTO_DOMROOT_FOCUS)

    def Frame(self, *locators):
        arg = [l.asMap() for l in locators]
        response = self._send_request(SetuActionType.GUIAUTO_DOMROOT_CREATE_FRAME, SetuArg.arg("locators", arg))
        return DefaultFrame(self._get_test_session(), self._get_automator(), response.getValueForElementSetuId())

    def Parent(self):
        raise Exception("DOM root does not have a parent frame.")


class AbstractBasicWindow(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def get_title(self):
        response = self._send_request(SetuActionType.GUIAUTO_WINDOW_GET_TITLE)
        return response.get_value_for_key("title").as_string()

    def focus(self):
        self._send_request(SetuActionType.GUIAUTO_WINDOW_FOCUS)


class DefaultChildWindow(AbstractBasicWindow):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def close(self):
        self._send_request(SetuActionType.GUIAUTO_CHILD_WINDOW_CLOSE)

    def MainWindow(self):
        return self._get_automator().MainWindow()


class DefaultMainWindow(AbstractBasicWindow):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def maximize(self):
        self._send_request(SetuActionType.GUIAUTO_MAIN_WINDOW_MAXIMIZE)

    def _take_element_finding_action(self, setu_action_type, *setu_args):
        response = self._send_request(setu_action_type, *setu_args)
        return response.getValueForElementSetuId()

    def ChildWindow(self, *withLocators):
        arg = [l.asMap() for l in withLocators]
        response = self._send_request(SetuActionType.GUIAUTO_MAIN_WINDOW_CREATE_CHILD_WINDOW, SetuArg.arg("locators", arg))
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.getValueForElementSetuId())

    def LatestChildWindow(self):
        response = self._send_request(SetuActionType.GUIAUTO_MAIN_WINDOW_GET_LATEST_CHILD_WINDOW)
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.getValueForElementSetuId())

    def close_all_child_windows(self):
        self._send_request(SetuActionType.GUIAUTO_MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS)
