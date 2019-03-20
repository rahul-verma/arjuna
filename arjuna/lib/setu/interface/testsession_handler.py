from arjuna.lib.setu.core.test.testsession import TestSession
from .guiautomator_handler import GuiAutomatorHandler
from arjuna.lib.setu.core.constants import SetuConfigOption
from arjuna.lib.setu.dispatcher.testsession import TestSessionDispatcher
from .gui_handler import GuiHandlerManager

class TestSessionHandler:

    def __init__(self):
        self.__testsession = None
        self.__automator_handlers = {}
        self.__conf_handler = None
        self.__databroker_handler = None
        self.__dispatcher = TestSessionDispatcher()
        self.__project_config_loaded = False
        self.__guimgr = None

    def __register_gui_automator_handler(self, handler):
        self.__automator_handlers[handler.setu_id] = handler

    def __deregister_gui_automator_handler(self, handler):
        del self.__automator_handlers[handler.setu_id]

    def __get_gui_automator_handler(self, setu_id):
        return self.__automator_handlers[setu_id]

    @property
    def setu_id(self):
        return self.__testsession.setu_id

    def init(self, root_dir):
        self.__testsession = TestSession()
        self.__testsession.init(root_dir)
        self.__conf_handler = TestSessionConfHandler(self.__testsession.configurator)
        self.__databroker_handler = TestSessionDataBrokerHandler(self.__testsession.data_broker)
        config_setu_id = self.__testsession.configurator.create_project_conf()
        self.__guimgr = GuiHandlerManager(self.__testsession.configurator.get_config(config_setu_id))
        return config_setu_id

    def __return_and_remove_arg(self, json_args_dict, key, optional=False):
        try:
            value = json_args_dict[key]
            del json_args_dict[key]
            return value
        except Exception as e:
            print(e)
            if optional: 
                return None
            else: 
                raise Exception("Input value for {} not found in JSON args: {}.".format(key, json_args_dict))

    def get_automator_handler(self, json_dict):
        return self.__automator_handlers[self.__return_and_remove_arg(json_dict, "automatorSetuId")]

    def get_gui_handler(self, json_dict):
        return self.__guimgr.get_gui_handler(self.__return_and_remove_arg(json_dict, "guiSetuId"))

    def get_element_setuid(self, json_dict):
        return self.__return_and_remove_arg(json_dict, "elementSetuId")

    def get_config_setuid(self, json_dict):
        return self.__return_and_remove_arg(json_dict, "configSetuId")

    def get_extended_config(self, json_dict):
        return self.__return_and_remove_arg(json_dict, "extendedConfig", optional=True)

    def take_session_action(self, action, json_dict):
        return getattr(self, action)(json_dict)

    def launch_guiautomator(self, json_dict):
        config_setu_id = self.get_config_setuid(json_dict)
        config = self.__testsession.configurator.get_config(config_setu_id)
        extended_config = self.get_extended_config(json_dict)
        handler = GuiAutomatorHandler(self.__dispatcher)
        handler.launch_automator(config, extended_config)
        self.__register_gui_automator_handler(handler)
        return {'automatorSetuId' : handler.setu_id}

    def quit_guiautomator(self, json_dict):
        auto_handler = self.get_automator_handler(json_dict)
        auto_handler.quit()
        self.__deregister_gui_automator_handler(auto_handler) 

    def register_config(self, json_dict):
        # Registering a config is post project conf registration. If no project conf, set it to true.
        self.__project_config_loaded = True
        setu_options = self.__return_and_remove_arg(json_dict, 'setuOptions')
        has_parent = self.__return_and_remove_arg(json_dict, 'hasParent')
        user_options = self.__return_and_remove_arg(json_dict, 'userOptions', optional=True)
        parent_config_id = self.__return_and_remove_arg(json_dict, 'parentConfigId', optional=True)
        return {"configSetuId" : self.__testsession.configurator.register_config(setu_options, has_parent, user_options, parent_config_id)} 

    def create_file_data_source(self, json_dict):
        file_name = self.__return_and_remove_arg(json_dict, 'fileName')
        record_type = self.__return_and_remove_arg(json_dict, 'recordType')
        data_dir = self.__testsession.configurator.get_central_setu_option_value(SetuConfigOption.DATA_SOURCES_DIR.name)
        return {"dataSourceSetuId" : self.__testsession.data_broker.create_file_data_source(data_dir, file_name, record_type, **json_dict)}  

    def create_gui(self, json_dict):
        auto_handler = self.get_automator_handler(json_dict)
        gui = self.__guimgr.create_gui(auto_handler, json_dict)
        return {"guiSetuId" : gui.setu_id}
    '''
        Delegating calls to its handlers.
    '''

    def take_conf_action(self, action, json_dict):
        return getattr(self.__conf_handler, action)(**json_dict)    

    def take_datasource_action(self, action, json_dict):
        return getattr(self.__databroker_handler, action)(**json_dict) 

    def take_automator_action(self, action, json_dict):
        handler = self.get_automator_handler(json_dict)
        gui_setu_id = json_dict.get("guiSetuId", None)
        if gui_setu_id is not None:
            handler = self.get_gui_handler(json_dict)
        print(action, json_dict)
        return getattr(handler, action)(**json_dict)

    def take_browser_action(self, action, json_dict):
        handler = self.get_automator_handler(json_dict)
        return handler.take_browser_action(action, json_dict) 

    def take_domroot_action(self, action, json_dict):
        handler = self.get_automator_handler(json_dict)
        return handler.take_domroot_action(action, json_dict) 

    '''
        Direct hand-over to same named methods in Gui automation handler
        after extraction of elementSetuId.
    '''

    def __take_automator_element_action(self, guiauotohandler_func, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)

        gui_setu_id = json_dict.get("guiSetuId", None)
        if gui_setu_id is not None:
            handler = self.get_gui_handler(json_dict)
            return getattr(handler, guiauotohandler_func)(action,elem_setu_id, json_dict) 

        gui_setu_id = json_dict.get("automatorSetuId", None)
        if gui_setu_id is not None:
            handler = self.get_automator_handler(json_dict)
            return getattr(handler, guiauotohandler_func)(action,elem_setu_id, json_dict) 

        raise Exception("For gui component action either guiSetuId or automatorSetuId must be provided.")

    def take_element_action(self, action, json_dict):
        return self.__take_automator_element_action("take_element_action", action, json_dict)

    def take_multielement_action(self, action, json_dict):
        return self.__take_automator_element_action("take_multielement_action", action, json_dict)

    def take_dropdown_action(self, action, json_dict):
        return self.__take_automator_element_action("take_dropdown_action", action, json_dict)

    def take_radiogroup_action(self, action, json_dict):
        return self.__take_automator_element_action("take_radiogroup_action", action, json_dict)

    def take_frame_action(self, action, json_dict):
        return self.__take_automator_element_action("take_frame_action", action, json_dict)

    def take_window_action(self, action, json_dict):
        return self.__take_automator_element_action("take_window_action", action, json_dict)

    def take_main_window_action(self, action, json_dict):
        return self.__take_automator_element_action("take_main_window_action", action, json_dict)

    def take_child_window_action(self, action, json_dict):
        return self.__take_automator_element_action("take_child_window_action", action, json_dict)

    def take_alert_action(self, action, json_dict):
        return self.__take_automator_element_action("take_alert_action", action, json_dict)

class TestSessionConfHandler:

    def __init__(self, configurator):
        self.__configurator = configurator

    def get_setu_option_value(self, configSetuId, option):
        return {"value" : self.__configurator.get_setu_option_value(configSetuId, option)}

class TestSessionDataBrokerHandler:

    def __init__(self, data_broker):
        self.__data_broker = data_broker

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