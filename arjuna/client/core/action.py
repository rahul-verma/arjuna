from enum import Enum, auto

class ConfigActionType(Enum):
	REGISTER_NEW_CONFIG = auto()
	GET_ARJUNA_OPTION_VALUE = auto()
	GET_USER_OPTION_VALUE = auto()


class DataSourceActionType(Enum):
	CREATE_FILE_DATA_SOURCE = auto()
	GET_NEXT_RECORD = auto()
	GET_ALL_RECORDS = auto()
	RESET = auto()

class GuiActionType(Enum):
	CREATE_GUI = auto()
	CREATE_CHILD_GUI = auto()

class GuiAutoActionType(Enum):
    LAUNCH = auto()
    QUIT= auto()
    SET_SLOMO = auto()
    EXECUTE_SCRIPT = auto()

    DEFINE = auto()

    GO_TO_URL = auto()
    GO_BACK = auto()
    GO_FORWARD = auto()
    REFRESH_CONTENT = auto()

    GET_SOURCE = auto()

    GET_ROOT_CONTENT = auto()
    GET_FULL_CONTENT = auto()
    GET_INNER_CONTENT = auto()
    GET_TEXT_CONTENT  = auto()

    ENTER_TEXT = auto()
    SET_TEXT = auto()
    CLEAR_TEXT = auto()

    CLICK = auto() 

    IDENTIFY = auto()

    WAIT_UNTIL_PRESENT = auto()
    WAIT_UNTIL_VISIBLE = auto()
    WAIT_UNTIL_CLICKABLE = auto() 

    CHECK = auto()
    UNCHECK = auto()

    CONFIGURE = auto()

    GET_INSTANCE_COUNT = auto()
    GET_RANDOM_INDEX = auto()

    HAS_VALUE_SELECTED = auto()
    HAS_INDEX_SELECTED = auto()
    GET_FIRST_SELECTED_OPTION_VALUE = auto()
    SELECT_BY_VALUE = auto()
    SELECT_BY_INDEX = auto() 

    SET_OPTION_LOCATORS = auto()
    SET_OPTION_CONTAINER = auto()
    HAS_VISIBLE_TEXT_SELECTED = auto()
    GET_FIRST_SELECTED_OPTION_TEXT = auto()
    SELECT_BY_VISIBLE_TEXT = auto()
    SEND_OPTION_TEXT = auto()

    FOCUS = auto()

    CONFIRM = auto()
    DISMISS = auto()
    GET_TEXT = auto()
    SEND_TEXT = auto()

    GET_PARENT = auto()

    GET_TITLE = auto() 

    MAXIMIZE = auto()
    GET_LATEST_CHILD_WINDOW = auto()
    CLOSE_ALL_CHILD_WINDOWS = auto()

    CLOSE = auto()

class SetuActionType(Enum):
	HELLO = auto()
	EXIT = auto()

class TestSessionActionType(Enum):
	INIT = auto()
	END = auto()