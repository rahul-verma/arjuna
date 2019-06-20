from flask import request
from flask_restful import Resource
from .objmgr import SetuSvcObjectManager
from arjuna.setu.testsession.adapter import TestSessionHandler
from arjuna.client.core.config import ArjunaComponent
from arjuna.client.core.action import *
from arjuna.setuext.guiauto.adapter.automator import GuiAutomatorHandler

from arjuna.setu import Setu
from arjuna.setu.adapter import Handler

import os

def create_success_response(data):
    res = {'result': 'success', 'responseData': data}, 200
    Setu.get_logger().debug("Setu Action Response: {}".format(res))
    return res


def create_error_response(emsg, etrace=None):
    etrace = etrace and etrace or "na"
    res = {'result': 'error', 'emessage': emsg, 'etrace': str(etrace)}, 500
    Setu.get_logger().debug("Setu Action Response (Error): {}".format(res))
    return res

component_action_map = {
    "SETU" : SetuActionType,
	"TEST_SESSION" : TestSessionActionType,
	"CONFIGURATOR" : ConfigActionType,
	"DATA_SOURCE" : DataSourceActionType,
	"GUI_AUTOMATOR" : GuiAutoActionType,
	"GUI" : GuiActionType
}

ACTION_HANDLER_MAP = {
    "SETU" : "_handle_setu_action",
    "TEST_SESSION" : "_handle_test_session_action",
    "CONFIGURATOR" : "_handle_configurator_action",
    "DATA_SOURCE" : "_handle_data_source_action",
    "GUI_AUTOMATOR" : "_handle_gui_automator_action",
    "GUI" : "_handle_gui_action"
}

class SetuSvc(Resource):

    def post(self):
        json_dict = request.get_json(force=True)
        Setu.get_logger().debug("Setu Action Request: {}".format(json_dict))
        json_component = json_dict["component"]
        json_action = json_dict["action"]
        action_type = None
        try:
            action_type = component_action_map[json_component][json_action.strip().upper()]
        except:
            return {'result': 'error', 'emessage': 'Invalid Setu action: Component: {} Action: {}'.format(json_component, json_action), 'etrace': 'NA'}, 500
        else:
            json_args = json_dict.get("args", {})
            return self.__call_handler(json_component, action_type, json_args)

    def __register_test_session(self, root_dir, cliConfig=None):
        handler = TestSessionHandler()

        config = handler.init(root_dir, cliConfig)
        SetuSvcObjectManager.register_testsession_handler(handler)
        out = {
            'testSessionSetuId': handler.setu_id,
            'configSetuId': config.setu_id,

        }

        out.update(config.as_json_dict())
        return out

    def __get_testsession_handler(self, component, action_type, json_args):
        try:
            tsession_id = json_args["testSessionSetuId"]
        except:
            return None, 'You must supply test session id in args for action {} for component {}. Your supplied JSON: {}'.format(action_type.name, component, json_args)
        else:
            handler = SetuSvcObjectManager.get_testsession_handler(tsession_id)
            del json_args["testSessionSetuId"]
            return handler, None

    def __call_handler(self, component, action_type, json_args):
        if component == "SETU":
            return self._handle_setu_action(action_type, json_args)
        elif component == "TEST_SESSION":
            return self._handle_test_session_action(action_type, json_args)
        else:
            testsession_handler, err = self.__get_testsession_handler(component, action_type, json_args)
            if not testsession_handler:
                return create_error_response(err)
            try:
                res = getattr(SetuSvc, ACTION_HANDLER_MAP[component])(
                    self,
                    testsession_handler,
                    action_type,
                    json_args
                )
            except Exception as f:
                import traceback
                ftrace = traceback.format_exc()
                return create_error_response(str(f), ftrace)
            else:
                return create_success_response(res)

    def _handle_setu_action(self, action_type, json_args):
        if action_type == SetuActionType.HELLO:
            return create_success_response({'value' : 'hello'})
        elif action_type == SetuActionType.EXIT:
            if not SetuSvcObjectManager.has_active_testsession():
                if os.name == 'nt':
                    os.system("taskkill /PID " + str(os.getpid()) + " /F")
                else :
                    os.system("kill " + str(os.getpid()))

    def _handle_test_session_action(self, action_type, json_args):
        if action_type == TestSessionActionType.INIT:
            try:
                root_dir = json_args["projectRootDir"]
                del json_args["projectRootDir"]
                res = self.__register_test_session(root_dir, **json_args)
                return create_success_response(res)
            except Exception as e:
                import traceback
                etrace = traceback.format_exc()
                return create_error_response(str(e), etrace)
        elif action_type == TestSessionActionType.END:
            pass

    def _handle_configurator_action(self, ts_handler, action_type, json_args):
        return ts_handler.conf_handler.take_action(action_type.name, json_args)

    def _handle_data_source_action(self, ts_handler, action_type, json_args):
        return ts_handler.datasource_handler.take_action(action_type, json_args)

    def _handle_gui_automator_action(self, ts_handler, action_type, json_args):
        if action_type == GuiAutoActionType.LAUNCH_AUTOMATOR:
            config = ts_handler.conf_handler.configurator.get_config(Handler.get_config_setuid(json_args))
            automator_handler = GuiAutomatorHandler(ts_handler.dispatcher)
            automator_handler.launch_automator(config, **json_args)
            ts_handler.register_gui_automator_handler(automator_handler)
            return {'automatorSetuId' : automator_handler.setu_id}
        elif action_type == GuiAutoActionType.QUIT_AUTOMATOR:
            handler = ts_handler.get_automator_handler(json_args)
            handler.quit_automator()
            ts_handler.deregister_gui_automator_handler(handler) 
        else:
            gui_setu_id = json_args.get("guiSetuId", None)
            handler = None
            if gui_setu_id is not None:
                handler = ts_handler.get_gui_handler(json_args)
            else:
                gui_automator_setu_id = json_args.get("automatorSetuId", None)
                if gui_automator_setu_id is None:
                    raise Exception("For gui component action either guiSetuId or automatorSetuId must be provided.")
                handler = ts_handler.get_automator_handler(json_args)
            return handler.take_action(action_type, json_args)

    def _handle_gui_action(self, ts_handler, action_type, json_args):
        automator_handler = ts_handler.get_automator_handler(json_args)
        return ts_handler.gui_manager.take_action(automator_handler, action_type, json_args)