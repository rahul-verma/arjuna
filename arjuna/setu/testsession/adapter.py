import logging
from arjuna.setu.testsession.impl import TestSession
from arjuna.setuext.guiauto.adapter.automator import GuiAutomatorHandler
from arjuna.tpi.enums import ArjunaOption
from arjuna.setu.dispatcher.testsession import TestSessionDispatcher
from arjuna.setuext.guiauto.adapter.gui import GuiHandlerManager
from arjuna.setu import Setu
from arjuna.setu.adapter import Handler


class TestSessionHandler(Handler):

    def __init__(self):
        self.__testsession = None
        self.__automator_handlers = {}
        self.__conf_handler = None
        self.__databroker_handler = None
        self.__dispatcher = TestSessionDispatcher()
        self.__project_config_loaded = False
        self.__guimgr = None

    def register_gui_automator_handler(self, handler):
        self.__automator_handlers[handler.setu_id] = handler

    def deregister_gui_automator_handler(self, handler):
        del self.__automator_handlers[handler.setu_id]

    def __get_gui_automator_handler(self, setu_id):
        return self.__automator_handlers[setu_id]

    @property
    def setu_id(self):
        return self.__testsession.setu_id

    def init(self, root_dir, cliConfig=None):
        self.__testsession = TestSession()
        self.__testsession.init(root_dir, cliConfig)
        config = self.__testsession.configurator.create_project_conf()
        Setu.init_logger(self.__testsession.setu_id, config.setu_config.value(ArjunaOption.LOG_DIR))
        self.__conf_handler = TestSessionConfHandler(self.__testsession.configurator)
        self.__databroker_handler = TestSessionDataBrokerHandler(self, self.__testsession.data_broker)
        self.__guimgr = GuiHandlerManager(config)
        return config

    @property
    def conf_handler(self):
        return self.__conf_handler

    @property
    def datasource_handler(self):
        return self.__databroker_handler

    @property
    def dispatcher(self):
        return self.__dispatcher

    @property
    def gui_manager(self):
        return self.__guimgr

    def get_automator_handler(self, json_dict):
        return self.__get_gui_automator_handler(self._pop_arg(json_dict, "automatorSetuId"))

    def get_gui_handler(self, json_dict):
        return self.__guimgr.get_gui_handler(self._pop_arg(json_dict, "guiSetuId"))

    def take_session_action(self, action, json_dict):
        return getattr(self, action)(json_dict)

class TestSessionConfHandler(Handler):

    def __init__(self, configurator):
        self.__configurator = configurator

    @property
    def configurator(self):
        return self.__configurator

    def take_action(self, action, json_args):
        return getattr(self, action.lower())(**json_args)

    def register_new_config(self, arjunaOptions, userOptions=None, hasParent=False, parentConfigId=None):
        # Registering a config is post project conf registration. If no project conf, set it to true.
        self.__project_config_loaded = True
        config = self.__configurator.register_config(arjunaOptions, userOptions, hasParent, parentConfigId)
        out_map = {'configSetuId' : config.setu_id}
        out_map.update(config.as_json_dict())
        return out_map

    def get_arjuna_option_value(self, configSetuId, option):
        return {"value": self.__configurator.get_arjuna_option_value(configSetuId, option)}

    def get_user_option_value(self, configSetuId, option):
        return {"value": self.__configurator.get_user_option_value(configSetuId, option)}


class TestSessionDataBrokerHandler(Handler):

    def __init__(self, testsession_handler, data_broker):
        self.__data_broker = data_broker
        self.__testsession_handler = testsession_handler

    def take_action(self, action_type, json_dict):
        return getattr(self, action_type.name.lower())(**json_dict) 

    def create_file_data_source(self, fileName, recordType, **json_dict):
        data_dir = self.__testsession_handler.conf_handler.configurator.get_central_arjuna_option_value(ArjunaOption.DATA_SOURCES_DIR.name)
        return {"dataSourceSetuId" : self.__data_broker.create_file_data_source(data_dir, fileName, recordType, **json_dict)}  

    def get_next_record(self, sourceSetuId):
        try:
            return {"finished" : False, "record" : self.__data_broker.get_next_record(sourceSetuId)}
        except Exception:
            return {"finished" : True}

    def get_all_records(self, sourceSetuId):
        try:
            return {"records" : self.__data_broker.get_all_records(sourceSetuId)}
        except Exception:
            return {"finished" : True}

    def reset(self, sourceSetuId):
        return {"finished" : False, "record" : self.__data_broker.reset(sourceSetuId)}