from enum import Enum, auto
from .connector import BaseSetuObject, SetuArg
from arjuna.lib.setu.core.constants import SetuConfigOption


class SetuActionType(Enum):
    TESTSESSION_INIT = auto()
    TESTSESSION_FINISH = auto()

    TESTSESSION_REGISTER_CONFIG = auto()

    TESTSESSION_CREATE_FILE_DATA_SOURCE = auto()

    TESTSESSION_LAUNCH_GUIAUTOMATOR = auto()
    TESTSESSION_QUIT_GUIAUTOMATOR = auto()

    TESTSESSION_CREATE_GUI = auto()

    CONFIGURATOR_GET_SETU_OPTION_VALUE = auto()
    CONFIGURATOR_GET_USER_OPTION_VALUE = auto()

    DATASOURCE_GET_NEXT_RECORD = auto()
    DATASOURCE_GET_ALL_RECORDS = auto()
    DATASOURCE_RESET = auto()

    GUIAUTO_BROWSER_GO_TO_URL = auto()
    GUIAUTO_BROWSER_GO_BACK = auto()
    GUIAUTO_BROWSER_GO_FORWARD = auto()
    GUIAUTO_BROWSER_REFRESH = auto()
    GUIAUTO_BROWSER_EXECUTE_JAVASCRIPT = auto()

    GUIAUTO_CREATE_ELEMENT = auto()
    GUIAUTO_CREATE_MULTIELEMENT = auto()
    GUIAUTO_CREATE_DROPDOWN = auto()
    GUIAUTO_CREATE_RADIOGROUP = auto()
    GUIAUTO_CREATE_FRAME = auto()
    GUIAUTO_CREATE_ALERT = auto()

    GUIAUTO_GET_MAIN_WINDOW = auto()
    GUIAUTO_SET_SLOMO = auto()

    GUIAUTO_ALERT_CONFIRM = auto()
    GUIAUTO_ALERT_DISMISS = auto()
    GUIAUTO_ALERT_GET_TEXT = auto()
    GUIAUTO_ALERT_SEND_TEXT = auto()

    GUIAUTO_GUI_CREATE_GUI = auto()

    GUIAUTO_ELEMENT_ENTER_TEXT = auto()
    GUIAUTO_ELEMENT_SET_TEXT = auto()
    GUIAUTO_ELEMENT_CLEAR_TEXT = auto()

    GUIAUTO_ELEMENT_CLICK = auto()

    GUIAUTO_ELEMENT_WAIT_UNTIL_CLICKABLE = auto()

    GUIAUTO_ELEMENT_CHECK = auto()
    GUIAUTO_ELEMENT_UNCHECK = auto()

    GUIAUTO_DROPDOWN_HAS_VALUE_SELECTED = auto()
    GUIAUTO_DROPDOWN_HAS_INDEX_SELECTED = auto()
    GUIAUTO_DROPDOWN_SELECT_BY_VALUE = auto()
    GUIAUTO_DROPDOWN_SELECT_BY_INDEX = auto()
    GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE  = auto()
    GUIAUTO_DROPDOWN_HAS_VISIBLE_TEXT_SELECTED = auto()
    GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT = auto()
    GUIAUTO_DROPDOWN_SELECT_BY_VISIBLE_TEXT = auto()

    GUIAUTO_RADIOGROUP_HAS_VALUE_SELECTED = auto()
    GUIAUTO_RADIOGROUP_HAS_INDEX_SELECTED = auto()
    GUIAUTO_RADIOGROUP_SELECT_BY_VALUE = auto()
    GUIAUTO_RADIOGROUP_SELECT_BY_INDEX = auto()
    GUIAUTO_RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE  = auto()

    GUIAUTO_DOMROOT_FOCUS = auto()
    GUIAUTO_DOMROOT_CREATE_FRAME = auto()

    GUIAUTO_FRAME_FOCUS = auto()
    GUIAUTO_FRAME_CREATE_FRAME = auto()
    GUIAUTO_FRAME_GET_PARENT = auto()

    GUIAUTO_WINDOW_FOCUS = auto()
    GUIAUTO_WINDOW_GET_TITLE = auto()

    GUIAUTO_MAIN_WINDOW_MAXIMIZE = auto()
    GUIAUTO_MAIN_WINDOW_CREATE_CHILD_WINDOW = auto()
    GUIAUTO_MAIN_WINDOW_GET_LATEST_CHILD_WINDOW = auto()
    GUIAUTO_MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS = auto()

    GUIAUTO_CHILD_WINDOW_CLOSE = auto()


class BaseConfig(BaseSetuObject):

    def __init__(self, test_session, name, setu_id):
        super().__init__()
        self.__session = test_session
        self.__name = name

        self._set_setu_id(setu_id)
        self._set_self_setu_id_arg("configSetuId")
        self._set_test_session_setu_id_arg(self.__session.getSetuId())

    def getTestSession(self):
        return self.__session

    def __fetch_config_option_value(self, setu_action_type, option_str):
        response = self._send_request(setu_action_type, SetuArg.arg("option", option_str))
        return response.getValue()

    def __normalize_option_str(self, option_str):
        return option_str.upper().strip().replace(".", "_")

    def __normalize_setu_option_str(self, option_str):
        return SetuConfigOption[self.__normalize_option_str(option_str)]

    def getSetuOptionValue(self, option):
        setu_option = option
        if type(option) is str:
            setu_option = self.__normalize_setu_option_str(option)
        return self.__fetch_config_option_value(SetuActionType.CONFIGURATOR_GET_SETU_OPTION_VALUE, setu_option.name)

    def getUserOptionValue(self, option):
        user_option = self.__normalize_option_str(option)
        return self.__fetch_config_option_value(SetuActionType.CONFIGURATOR_GET_USER_OPTION_VALUE, user_option)

    def getName(self):
        return self.__name





