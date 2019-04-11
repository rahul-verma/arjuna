from flask import request
from flask_restful import Resource
from .objmgr import SetuSvcObjectManager
from arjuna.lib.setu.testsession.adapter import TestSessionHandler
from arjuna.lib.setu.core.requester.config import SetuActionType

from arjuna.lib.setu import Setu


def create_success_response(data):
    res = {'result': 'success', 'responseData': data}, 200
    Setu.get_logger().debug("Setu Action Response: {}".format(res))
    return res


def create_error_response(emsg, etrace=None):
    etrace = etrace and etrace or "na"
    res = {'result': 'error', 'emessage': emsg, 'etrace': str(etrace)}, 500
    Setu.get_logger().debug("Setu Action Response (Error): {}".format(res))
    return res


class SetuSvc(Resource):

    def post(self):
        json_dict = request.get_json(force=True)
        Setu.get_logger().debug("Setu Action Request: {}".format(json_dict))
        json_action = json_dict["action"]
        try:
            action_type = SetuActionType[json_action.upper().strip()]
        except:
            return {'result': 'error', 'emessage': 'Invalid Setu action: {}'.format(json_action), 'etrace': 'NA'}, 500
        else:
            if action_type == SetuActionType.TESTSESSION_INIT:
                try:
                    root_dir = json_dict["args"]["projectRootDir"]
                    del json_dict["args"]["projectRootDir"]
                    res = self.__register_test_session(root_dir, **json_dict["args"])
                    return create_success_response(res)
                except Exception as e:
                    import traceback
                    etrace = traceback.format_exc()
                    return create_error_response(str(e), etrace)
            elif action_type == SetuActionType.TESTSESSION_FINISH:
                pass
            else:
                testsession_handler, err = self.__get_testsession_handler(json_dict)
                if not testsession_handler:
                    return create_error_response(err)
                try:
                    res = self.__call_test_session_handler(testsession_handler, action_type, json_dict)
                except Exception as f:
                    import traceback
                    ftrace = traceback.format_exc()
                    return create_error_response(str(f), ftrace)
                else:
                    return create_success_response(res)

    def __register_test_session(self, root_dir, cliConfig=None):
        handler = TestSessionHandler()

        config_id = handler.init(root_dir, cliConfig)
        SetuSvcObjectManager.register_testsession_handler(handler)
        return {
            'testSessionSetuId': handler.setu_id,
            'configSetuId': config_id
        }

    def __get_testsession_handler(self, json_dict):
        try:
            tsession_id = json_dict["args"]["testSessionSetuId"]
        except:
            return None, 'You must supply test session id in args for this action. Your supplied JSON: {}'.format(json_dict)
        else:
            handler = SetuSvcObjectManager.get_testsession_handler(tsession_id)
            del json_dict["args"]["testSessionSetuId"]
            return handler, None

    def __call_test_session_handler(self, handler: TestSessionHandler, action_type, json_dict):
        handler_remove_prefix = {
            handler.take_session_action: "TESTSESSION_",
            handler.take_conf_action: "CONFIGURATOR_",
            handler.take_datasource_action: "DATASOURCE_",
            handler.take_browser_action: "GUIAUTO_BROWSER_",
            handler.take_domroot_action: "GUIAUTO_DOMROOT_",
            handler.take_automator_action: "GUIAUTO_",
            handler.take_alert_action: "GUIAUTO_ALERT_",
            handler.take_element_action: "GUIAUTO_ELEMENT_",
            handler.take_dropdown_action: "GUIAUTO_DROPDOWN_",
            handler.take_radiogroup_action: "GUIAUTO_RADIOGROUP_",
            handler.take_frame_action: "GUIAUTO_FRAME_",
            handler.take_window_action: "GUIAUTO_WINDOW_",
            handler.take_main_window_action: "GUIAUTO_MAIN_WINDOW_",
            handler.take_child_window_action: "GUIAUTO_CHILD_WINDOW_",
            handler.take_gui_action: "GUIAUTO_GUI_"
        }

        action_method_map = {
            SetuActionType.TESTSESSION_REGISTER_CONFIG: handler.take_session_action,
            
            SetuActionType.TESTSESSION_CREATE_FILE_DATA_SOURCE: handler.take_session_action,
            
            SetuActionType.TESTSESSION_LAUNCH_GUIAUTOMATOR: handler.take_session_action,
            SetuActionType.TESTSESSION_QUIT_GUIAUTOMATOR: handler.take_session_action,

            SetuActionType.TESTSESSION_CREATE_GUI: handler.take_session_action,
            
            SetuActionType.CONFIGURATOR_GET_ARJUNA_OPTION_VALUE: handler.take_conf_action,
            SetuActionType.CONFIGURATOR_GET_USER_OPTION_VALUE: handler.take_conf_action,
            
            SetuActionType.DATASOURCE_GET_NEXT_RECORD: handler.take_datasource_action,
            SetuActionType.DATASOURCE_GET_ALL_RECORDS: handler.take_datasource_action,
            SetuActionType.DATASOURCE_RESET: handler.take_datasource_action,
            
            SetuActionType.GUIAUTO_BROWSER_GO_TO_URL: handler.take_browser_action,
            SetuActionType.GUIAUTO_BROWSER_GO_BACK: handler.take_browser_action,
            SetuActionType.GUIAUTO_BROWSER_GO_FORWARD: handler.take_browser_action,
            SetuActionType.GUIAUTO_BROWSER_REFRESH: handler.take_browser_action,
            SetuActionType.GUIAUTO_BROWSER_EXECUTE_JAVASCRIPT: handler.take_browser_action,
            
            SetuActionType.GUIAUTO_CREATE_ELEMENT: handler.take_automator_action,
            SetuActionType.GUIAUTO_CREATE_MULTIELEMENT: handler.take_automator_action,
            SetuActionType.GUIAUTO_CREATE_DROPDOWN: handler.take_automator_action,
            SetuActionType.GUIAUTO_CREATE_RADIOGROUP: handler.take_automator_action,
            SetuActionType.GUIAUTO_CREATE_FRAME: handler.take_automator_action,
            SetuActionType.GUIAUTO_CREATE_ALERT: handler.take_automator_action,
            
            SetuActionType.GUIAUTO_GET_MAIN_WINDOW: handler.take_automator_action,
            SetuActionType.GUIAUTO_SET_SLOMO: handler.take_automator_action,

            SetuActionType.GUIAUTO_ALERT_CONFIRM: handler.take_alert_action,
            SetuActionType.GUIAUTO_ALERT_DISMISS: handler.take_alert_action,
            SetuActionType.GUIAUTO_ALERT_GET_TEXT: handler.take_alert_action,
            SetuActionType.GUIAUTO_ALERT_SEND_TEXT: handler.take_alert_action,
            
            SetuActionType.GUIAUTO_GUI_CREATE_GUI: handler.take_gui_action,
            
            SetuActionType.GUIAUTO_ELEMENT_ENTER_TEXT: handler.take_element_action,
            SetuActionType.GUIAUTO_ELEMENT_SET_TEXT: handler.take_element_action,
            SetuActionType.GUIAUTO_ELEMENT_CLEAR_TEXT: handler.take_element_action,
        
            SetuActionType.GUIAUTO_ELEMENT_CLICK: handler.take_element_action,
            
            SetuActionType.GUIAUTO_ELEMENT_WAIT_UNTIL_CLICKABLE: handler.take_element_action,
            
            SetuActionType.GUIAUTO_ELEMENT_CHECK: handler.take_element_action,
            SetuActionType.GUIAUTO_ELEMENT_UNCHECK: handler.take_element_action,
            
            SetuActionType.GUIAUTO_DROPDOWN_HAS_VALUE_SELECTED: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_HAS_INDEX_SELECTED: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VALUE: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_INDEX: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE : handler.take_dropdown_action,        
            SetuActionType.GUIAUTO_DROPDOWN_HAS_VISIBLE_TEXT_SELECTED: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT: handler.take_dropdown_action,
            SetuActionType.GUIAUTO_DROPDOWN_SELECT_BY_VISIBLE_TEXT: handler.take_dropdown_action,

            SetuActionType.GUIAUTO_RADIOGROUP_HAS_VALUE_SELECTED: handler.take_radiogroup_action,
            SetuActionType.GUIAUTO_RADIOGROUP_HAS_INDEX_SELECTED: handler.take_radiogroup_action,
            SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_VALUE: handler.take_radiogroup_action,
            SetuActionType.GUIAUTO_RADIOGROUP_SELECT_BY_INDEX: handler.take_radiogroup_action,
            SetuActionType.GUIAUTO_RADIOGROUP_GET_FIRST_SELECTED_OPTION_VALUE : handler.take_radiogroup_action,

            SetuActionType.GUIAUTO_DOMROOT_FOCUS: handler.take_domroot_action,
            SetuActionType.GUIAUTO_DOMROOT_CREATE_FRAME: handler.take_domroot_action,
            
            SetuActionType.GUIAUTO_FRAME_FOCUS: handler.take_frame_action,
            SetuActionType.GUIAUTO_FRAME_CREATE_FRAME: handler.take_frame_action,
            SetuActionType.GUIAUTO_FRAME_GET_PARENT: handler.take_frame_action,
            
            SetuActionType.GUIAUTO_WINDOW_FOCUS: handler.take_window_action,
            SetuActionType.GUIAUTO_WINDOW_GET_TITLE: handler.take_window_action,
            
            SetuActionType.GUIAUTO_MAIN_WINDOW_MAXIMIZE: handler.take_main_window_action,
            SetuActionType.GUIAUTO_MAIN_WINDOW_CREATE_CHILD_WINDOW: handler.take_main_window_action,
            SetuActionType.GUIAUTO_MAIN_WINDOW_GET_LATEST_CHILD_WINDOW: handler.take_main_window_action,
            SetuActionType.GUIAUTO_MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS: handler.take_main_window_action,
            
            SetuActionType.GUIAUTO_CHILD_WINDOW_CLOSE: handler.take_child_window_action,
        }

        method = action_method_map[action_type]
        del json_dict["action"]
        return method(action_type.name.replace(handler_remove_prefix[method], "").lower(), json_dict["args"])
