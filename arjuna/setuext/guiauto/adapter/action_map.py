from arjuna.client.core.action import *


HANDLER_NAME_MAP = {
    1 : ("take_direct_action", ""),
    2 : ("take_browser_action", "BROWSER_"),
    3 : ("take_alert_action", "ALERT_"),
    4 : ("take_element_action", "ELEMENT_"),
    5 : ("take_dropdown_action", "DROPDOWN_"),
    6 : ("take_radiogroup_action", "RADIOGROUP_"),
    7 : ("take_domroot_action", "DOMROOT_"),
    8 : ("take_frame_action", "FRAME_"),
    9 : ("take_window_action", "WINDOW_"),
    10 : ("take_main_window_action", "MAIN_WINDOW_"),
    11 : ("take_child_window_action", "CHILD_WINDOW_")
}

HANDLER_MAP = {
    GuiAutoActionType.DEFINE_ELEMENT : 1,
    GuiAutoActionType.DEFINE_MULTIELEMENT : 1,
    GuiAutoActionType.DEFINE_DROPDOWN : 1,
    GuiAutoActionType.DEFINE_RADIOGROUP: 1,
    GuiAutoActionType.DEFINE_ALERT: 1,

    GuiAutoActionType.QUIT_AUTOMATOR: 1,
    
    GuiAutoActionType.BROWSER_GO_TO_URL: 2,
    GuiAutoActionType.BROWSER_GO_BACK: 2,
    GuiAutoActionType.BROWSER_GO_FORWARD: 2,
    GuiAutoActionType.BROWSER_REFRESH: 2,
    GuiAutoActionType.BROWSER_EXECUTE_JAVASCRIPT: 2,
    
    GuiAutoActionType.DEFINE_MAIN_WINDOW: 1,
    GuiAutoActionType.SET_SLOMO: 1,

    GuiAutoActionType.ALERT_CONFIRM: 3,
    GuiAutoActionType.ALERT_DISMISS: 3,
    GuiAutoActionType.ALERT_GET_TEXT: 3,
    GuiAutoActionType.ALERT_SEND_TEXT: 3,
    
    GuiAutoActionType.ELEMENT_ENTER_TEXT: 4,
    GuiAutoActionType.ELEMENT_SET_TEXT: 4,
    GuiAutoActionType.ELEMENT_CLEAR_TEXT: 4,

    GuiAutoActionType.ELEMENT_CLICK: 4,
    
    GuiAutoActionType.ELEMENT_WAIT_UNTIL_CLICKABLE: 4,
    
    GuiAutoActionType.ELEMENT_CHECK: 4,
    GuiAutoActionType.ELEMENT_UNCHECK: 4,
    
    GuiAutoActionType.DROPDOWN_HAS_VALUE_SELECTED: 5,
    GuiAutoActionType.DROPDOWN_HAS_INDEX_SELECTED: 5,
    GuiAutoActionType.DROPDOWN_SELECT_BY_VALUE: 5,
    GuiAutoActionType.DROPDOWN_SELECT_BY_INDEX: 5,
    GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE : 5,        
    GuiAutoActionType.DROPDOWN_HAS_VISIBLE_TEXT_SELECTED: 5,
    GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT: 5,
    GuiAutoActionType.DROPDOWN_SELECT_BY_VISIBLE_TEXT: 5,

    GuiAutoActionType.RADIOGROUP_HAS_VALUE_SELECTED: 6,
    GuiAutoActionType.RADIOGROUP_HAS_INDEX_SELECTED: 6,
    GuiAutoActionType.RADIOGROUP_SELECT_BY_VALUE: 6,
    GuiAutoActionType.RADIOGROUP_SELECT_BY_INDEX: 6,
    GuiAutoActionType.RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE : 6,

    GuiAutoActionType.DOMROOT_FOCUS: 7,
    GuiAutoActionType.DOMROOT_CREATE_FRAME: 7,
    
    GuiAutoActionType.FRAME_FOCUS: 8,
    GuiAutoActionType.FRAME_CREATE_FRAME: 8,
    GuiAutoActionType.FRAME_GET_PARENT: 8,
    
    GuiAutoActionType.WINDOW_FOCUS: 9,
    GuiAutoActionType.WINDOW_GET_TITLE: 9,
    
    GuiAutoActionType.MAIN_WINDOW_MAXIMIZE: 10,
    GuiAutoActionType.MAIN_WINDOW_CREATE_CHILD_WINDOW: 10,
    GuiAutoActionType.MAIN_WINDOW_GET_LATEST_CHILD_WINDOW: 10,
    GuiAutoActionType.MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS: 10,
    
    GuiAutoActionType.CHILD_WINDOW_CLOSE: 11,
}