from enum import Enum, auto

class SetuGuiAutoActorStateActionType(Enum):
    INIT_STATE = auto()
    END_STATE = auto()

class SetuGuiAutoActorAutomatorActionType(Enum):

    LAUNCH = auto()
    QUIT = auto()

    GO_TO_URL = auto()

    GO_BACK = auto()
    GO_FORWARD = auto()
    REFRESH = auto()
    EXECUTE_JAVASCRIPT = auto()

    FIND_ELEMENT = auto()
    FIND_MULTIELEMENT = auto()

    GET_CURRENT_WINDOW_HANDLE = auto()
    GET_WINDOW_TITLE = auto()
    MAXIMIZE_WINDOW = auto()
    GET_CURRENT_WINDOW_SIZE = auto()
    SET_WINDOW_SIZE = auto()
    GET_ALL_WINDOW_HANDLES = auto()
    SWITCH_TO_WINDOW = auto()
    CLOSE_CURRENT_WINDOW = auto()

    IS_ALERT_PRESENT = auto()
    CONFIRM_ALERT = auto()
    DISMISS_ALERT = auto()
    GET_TEXT_FROM_ALERT = auto()
    SEND_TEXT_TO_ALERT = auto()

    GET_CURRENT_VIEW_CONTEXT = auto()
    GET_ALL_VIEW_CONTEXTS = auto()
    SWITCH_TO_VIEW_CONTEXT = auto()

    JUMP_TO_FRAME = auto()
    JUMP_TO_PARENT_FRAME = auto()
    JUMP_TO_DOM_ROOT = auto()

class SetuGuiAutoActorElementActionType(Enum):
	FIND_MULTIELEMENT = auto()
	FIND_ELEMENT = auto()
	CLICK = auto()
	CLEAR_TEXT = auto()
	SEND_TEXT = auto()
	IS_SELECTED = auto()
	IS_VISIBLE = auto()
	IS_CLICKABLE = auto()
	GET_TAG_NAME = auto()
	GET_ATTR_VALUE = auto()
	GET_TEXT_CONTENT = auto()

class SetuActorDriverConfigOption(Enum):
    AUTOMATOR_NAME = auto()
    GUIAUTO_CONTEXT = auto()

    # Browser (Common)
    BROWSER_NAME = auto()
    BROWSER_BIN_PATH = auto()
    BROWSER_PROXY_ON = auto()
    BROWSER_PROXY_HOST = auto()
    BROWSER_PROXY_PORT = auto()
    MOBILE_OS_NAME = auto()

    # Selenium
    SELENIUM_DRIVER_PROP = auto()
    SELENIUM_DRIVER_PATH = auto()

    # Appium
    APPIUM_HUB_URL = auto()
    APPIUM_AUTO_LAUNCH = auto()