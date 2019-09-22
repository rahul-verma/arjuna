from arjuna.client.core.action import *
from enum import Enum, auto

class GuiInternalActionType(Enum):

    DEFINE_ELEMENT  = auto()
    DEFINE_MULTI_ELEMENT  = auto()
    DEFINE_DROPDOWN  = auto()
    DEFINE_RADIOGROUP = auto()
    DEFINE_ALERT = auto()

    QUIT_AUTOMATOR = auto()

    GET_SOURCE = auto()

    GET_ROOT_CONTENT = auto()
    GET_FULL_CONTENT = auto()
    GET_INNER_CONTENT = auto()
    GET_TEXT_CONTENT = auto()
    
    BROWSER_GO_TO_URL = auto()
    BROWSER_GO_BACK = auto()
    BROWSER_GO_FORWARD = auto()
    BROWSER_REFRESH = auto()
    EXECUTE_SCRIPT = auto()
    
    DEFINE_MAIN_WINDOW = auto()
    SET_SLOMO = auto()

    ALERT_CONFIRM = auto()
    ALERT_DISMISS = auto()
    ALERT_GET_TEXT = auto()
    ALERT_SEND_TEXT = auto()

    ELEMENT_GET_SOURCE = auto()    
    ELEMENT_ENTER_TEXT = auto()
    ELEMENT_SET_TEXT = auto()
    ELEMENT_CLEAR_TEXT = auto()

    ELEMENT_CLICK = auto()
    
    ELEMENT_IDENTIFY = auto()
    ELEMENT_WAIT_UNTIL_PRESENT = auto()
    ELEMENT_WAIT_UNTIL_VISIBLE = auto()
    ELEMENT_WAIT_UNTIL_CLICKABLE = auto()
    
    ELEMENT_CHECK = auto()
    ELEMENT_UNCHECK = auto()

    ELEMENT_GET_ROOT_SOURCE = auto()
    ELEMENT_GET_FULL_SOURCE = auto()
    ELEMENT_GET_INNER_SOURCE = auto()
    ELEMENT_GET_TEXT = auto()

    ELEMENT_CONFIGURE = auto()

    MULTI_ELEMENT_GET_INSTANCE_COUNT = auto()
    MULTI_ELEMENT_GET_RANDOM_INDEX = auto()
    
    DROPDOWN_CONFIGURE = auto()
    DROPDOWN_SET_OPTION_LOCATORS = auto()
    DROPDOWN_SET_OPTION_CONTAINER = auto()
    DROPDOWN_HAS_VALUE_SELECTED = auto()
    DROPDOWN_HAS_INDEX_SELECTED = auto()
    DROPDOWN_HAS_VISIBLE_TEXT_SELECTED = auto()
    DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE  = auto()        
    DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT = auto()
    DROPDOWN_SELECT_BY_VALUE = auto()
    DROPDOWN_SELECT_BY_INDEX = auto()
    DROPDOWN_SELECT_BY_VISIBLE_TEXT = auto()
    DROPDOWN_SEND_OPTION_TEXT = auto()
    DROPDOWN_GET_SOURCE = auto()

    RADIOGROUP_HAS_VALUE_SELECTED = auto()
    RADIOGROUP_HAS_INDEX_SELECTED = auto()
    RADIOGROUP_SELECT_BY_VALUE = auto()
    RADIOGROUP_SELECT_BY_INDEX = auto()
    RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE  = auto()
    RADIOGROUP_CONFIGURE  = auto()
    RADIOGROUP_GET_SOURCE = auto()

    DOMROOT_FOCUS = auto()
    DOMROOT_DEFINE_FRAME = auto()
    DOMROOT_GET_SOURCE = auto()
    
    FRAME_FOCUS = auto()
    FRAME_DEFINE_FRAME = auto()
    FRAME_GET_PARENT = auto()
    FRAME_GET_SOURCE = auto()
    
    MAIN_WINDOW_FOCUS = auto()
    MAIN_WINDOW_GET_TITLE = auto()
    MAIN_WINDOW_MAXIMIZE = auto()
    MAIN_WINDOW_DEFINE_CHILD_WINDOW = auto()
    MAIN_WINDOW_GET_LATEST_CHILD_WINDOW = auto()
    MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS = auto()

    CHILD_WINDOW_FOCUS = auto()
    CHILD_WINDOW_GET_TITLE = auto()    
    CHILD_WINDOW_CLOSE = auto()

HANDLER_NAME_MAP = {
    1 : ("take_direct_action", ""),
    2 : ("take_browser_action", "BROWSER_"),
    3 : ("take_alert_action", "ALERT_"),
    4 : ("take_element_action", "ELEMENT_"),
    5 : ("take_dropdown_action", "DROPDOWN_"),
    6 : ("take_radiogroup_action", "RADIOGROUP_"),
    7 : ("take_domroot_action", "DOMROOT_"),
    8 : ("take_frame_action", "FRAME_"),
    9 : ("take_source_action", "WINDOW_"),
    10 : ("take_main_window_action", "MAIN_WINDOW_"),
    11 : ("take_child_window_action", "CHILD_WINDOW_"),
    12 : ("take_multi_element_action", "MULTI_ELEMENT_"),
}

HANDLER_MAP = {
    GuiInternalActionType.DEFINE_ELEMENT : 1,
    GuiInternalActionType.DEFINE_MULTI_ELEMENT : 1,
    GuiInternalActionType.DEFINE_DROPDOWN : 1,
    GuiInternalActionType.DEFINE_RADIOGROUP: 1,
    GuiInternalActionType.DEFINE_ALERT: 1,

    GuiInternalActionType.QUIT_AUTOMATOR: 1,

    GuiInternalActionType.GET_SOURCE: 1,

    GuiInternalActionType.GET_ROOT_CONTENT: 9,
    GuiInternalActionType.GET_FULL_CONTENT: 9,
    GuiInternalActionType.GET_INNER_CONTENT: 9,
    GuiInternalActionType.GET_TEXT_CONTENT: 9,
    
    GuiInternalActionType.BROWSER_GO_TO_URL: 2,
    GuiInternalActionType.BROWSER_GO_BACK: 2,
    GuiInternalActionType.BROWSER_GO_FORWARD: 2,
    GuiInternalActionType.BROWSER_REFRESH: 2,
    GuiInternalActionType.EXECUTE_SCRIPT: 2,
    
    GuiInternalActionType.DEFINE_MAIN_WINDOW: 1,
    GuiInternalActionType.SET_SLOMO: 1,

    GuiInternalActionType.ALERT_CONFIRM: 3,
    GuiInternalActionType.ALERT_DISMISS: 3,
    GuiInternalActionType.ALERT_GET_TEXT: 3,
    GuiInternalActionType.ALERT_SEND_TEXT: 3,
    
    GuiInternalActionType.ELEMENT_GET_SOURCE: 4,
    GuiInternalActionType.ELEMENT_ENTER_TEXT: 4,
    GuiInternalActionType.ELEMENT_SET_TEXT: 4,
    GuiInternalActionType.ELEMENT_CLEAR_TEXT: 4,

    GuiInternalActionType.ELEMENT_CLICK: 4,
    
    GuiInternalActionType.ELEMENT_IDENTIFY: 4,
    GuiInternalActionType.ELEMENT_WAIT_UNTIL_PRESENT: 4,
    GuiInternalActionType.ELEMENT_WAIT_UNTIL_VISIBLE: 4,
    GuiInternalActionType.ELEMENT_WAIT_UNTIL_CLICKABLE: 4,
    
    GuiInternalActionType.ELEMENT_CHECK: 4,
    GuiInternalActionType.ELEMENT_UNCHECK: 4,

    GuiInternalActionType.ELEMENT_GET_ROOT_SOURCE: 4,
    GuiInternalActionType.ELEMENT_GET_FULL_SOURCE: 4,
    GuiInternalActionType.ELEMENT_GET_INNER_SOURCE: 4,
    GuiInternalActionType.ELEMENT_GET_TEXT: 4,

    GuiInternalActionType.ELEMENT_CONFIGURE: 4,

    GuiInternalActionType.MULTI_ELEMENT_GET_INSTANCE_COUNT: 12,
    GuiInternalActionType.MULTI_ELEMENT_GET_RANDOM_INDEX: 12,
    
    GuiInternalActionType.DROPDOWN_CONFIGURE: 5,
    GuiInternalActionType.DROPDOWN_GET_SOURCE: 5,
    GuiInternalActionType.DROPDOWN_SET_OPTION_LOCATORS: 5,
    GuiInternalActionType.DROPDOWN_SET_OPTION_CONTAINER: 5,
    GuiInternalActionType.DROPDOWN_HAS_VALUE_SELECTED: 5,
    GuiInternalActionType.DROPDOWN_HAS_INDEX_SELECTED: 5,
    GuiInternalActionType.DROPDOWN_HAS_VISIBLE_TEXT_SELECTED: 5,
    GuiInternalActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE : 5,        
    GuiInternalActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT: 5,
    GuiInternalActionType.DROPDOWN_SELECT_BY_VALUE: 5,
    GuiInternalActionType.DROPDOWN_SELECT_BY_INDEX: 5,
    GuiInternalActionType.DROPDOWN_SELECT_BY_VISIBLE_TEXT: 5,
    GuiInternalActionType.DROPDOWN_SEND_OPTION_TEXT: 5,

    GuiInternalActionType.RADIOGROUP_HAS_VALUE_SELECTED: 6,
    GuiInternalActionType.RADIOGROUP_HAS_INDEX_SELECTED: 6,
    GuiInternalActionType.RADIOGROUP_SELECT_BY_VALUE: 6,
    GuiInternalActionType.RADIOGROUP_SELECT_BY_INDEX: 6,
    GuiInternalActionType.RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE : 6,
    GuiInternalActionType.RADIOGROUP_CONFIGURE : 6,
    GuiInternalActionType.RADIOGROUP_GET_SOURCE: 6,

    GuiInternalActionType.DOMROOT_FOCUS: 7,
    GuiInternalActionType.DOMROOT_DEFINE_FRAME: 7,
    GuiInternalActionType.DOMROOT_GET_SOURCE: 7,
    
    GuiInternalActionType.FRAME_FOCUS: 8,
    GuiInternalActionType.FRAME_DEFINE_FRAME: 8,
    GuiInternalActionType.FRAME_GET_PARENT: 8,
    GuiInternalActionType.FRAME_GET_SOURCE: 8,

    GuiInternalActionType.MAIN_WINDOW_FOCUS: 10,  
    GuiInternalActionType.MAIN_WINDOW_GET_TITLE: 10, 
    GuiInternalActionType.MAIN_WINDOW_MAXIMIZE: 10,
    GuiInternalActionType.MAIN_WINDOW_DEFINE_CHILD_WINDOW: 10,
    GuiInternalActionType.MAIN_WINDOW_GET_LATEST_CHILD_WINDOW: 10,
    GuiInternalActionType.MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS: 10,

    GuiInternalActionType.CHILD_WINDOW_FOCUS: 11,  
    GuiInternalActionType.CHILD_WINDOW_GET_TITLE: 11,     
    GuiInternalActionType.CHILD_WINDOW_CLOSE: 11,
}