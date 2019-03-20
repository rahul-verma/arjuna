from arjuna.lib.setu.requester.connector import BaseSetuObject, SetuArg
from arjuna.lib.setu.requester.config import SetuActionType


class BaseComponent(BaseSetuObject):

    def __init__(self, test_session, app_automator):
        super().__init__()
        self.__test_session = test_session
        self.__automator = app_automator

        if app_automator.isGui():
            self._set_gui_setu_id_arg(app_automator.getSetuId())
        else:
            self._set_automator_setu_id_arg(app_automator.getSetuId())

        self._set_test_session_setu_id_arg(test_session.getSetuId())

    def _get_automator(self):
        return self.__automator

    def _get_test_session(self):
        return self.__test_session


class BaseElement(BaseComponent):

    def __init(self, test_session, app_automator, setu_id, index=None):
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

    def enterText(self, text):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_ENTER_TEXTs)

    def setText(self, text):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_ENTER_TEXT)

    def click(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_CLICK)

    def waitUntilClickable(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_WAIT_UNTIL_CLICKABLE)

    def check(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_CHECK)

    def uncheck(self):
        self._send_request(SetuActionType.GUIAUTO_ELEMENT_UNCHECK)


class DefaultGuiMultiElement(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def getInstanceAtIndex(self, index):
        return DefaultGuiElement(self._get_test_session(), self._get_automator(), self.getSetuId(), index)


class DefaultDropDown(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def hasValueSelected(self, value):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_VALUE_SELECTED, SetuArg.valueArg(value))
        return response.getValueForCheckResult()

    def hasIndexSelected(self, index):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_INDEX_SELECTED, SetuArg.indexArg(index))
        return response.getValueForCheckResult()

    def selectByValue(self, value):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VALUE, SetuArg.valueArg(value))

    def selectByIndex(self, index):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_INDEX, SetuArg.indexArg(index))

    def getFirstSelectedOptionValue(self):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.getValueForValueAttr()

    def getFirstSelectedOptionText(self):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT)
        return response.getValueForText()

    def hasVisibleTextSelected(self, text):
        response = self._send_request(SetuActionType.GUIAUTO_DROPDOWN_HAS_VISIBLE_TEXT_SELECTED, SetuArg.textArg(text))
        return response.getValueForCheckResult()

    def selectByVisibleText(self, text):
        self._send_request(SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VISIBLE_TEXT, SetuArg.textArg(text))


class DefaultRadioGroup(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def hasValueSelected(self, value):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_HAS_VALUE_SELECTED, SetuArg.valueArg(value))
        return response.getValueForCheckResult()

    def hasIndexSelected(self, index):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_HAS_INDEX_SELECTED, SetuArg.indexArg(index))
        return response.getValueForCheckResult()

    def selectByValue(self, value):
        self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_VALUE, SetuArg.valueArg(value))

    def selectByIndex(self, index):
        self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_INDEX, SetuArg.indexArg(index))

    def getFirstSelectedOptionValue(self):
        response = self._send_request(SetuActionType.GUIAUTO_RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.getValueForValueAttr()


class DefaultAlert(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def confirm(self):
        self._send_request(SetuActionType.GUIAUTO_ALERT_CONFIRM)

    def dismiss(self):
        self._send_request(SetuActionType.GUIAUTO_ALERT_DISMISS)

    def getText(self):
        response = self._send_request(SetuActionType.GUIAUTO_ALERT_GET_TEXT)
        return response.getValueForText()

    def sendText(self, text):
        self._send_request(SetuActionType.GUIAUTO_ALERT_SEND_TEXT, SetuArg.textArg(text))


class DefaultBrowser(BaseElement):

    def __init__(self, test_session, app_automator, setu_id):
        super().__init__(test_session, app_automator, setu_id)

    def goToUrl(self, url):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_TO_URL, SetuArg.arg("url", url))

    def goBack(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_BACK)

    def goForward(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_GO_FORWARD)

    def refresh(self):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_REFRESH)