from arjuna.client.core.connector import SetuArg
from arjuna.lib.config import DefaultTestConfig
from arjuna.client.core.connector import BaseSetuObject
from arjuna.client.core.action import *
from arjuna.client.core.config import ArjunaComponent

class DefaultTestSession(BaseSetuObject):
    
    def __init__(self):
        super().__init__()
        self.__DEF_CONF_NAME = "central"

    def init(self, project_root_dir, cli_config, runid):
        super().__init__()
        args = [SetuArg.arg("projectRootDir", project_root_dir)]
        if cli_config:
            args.append(SetuArg.arg("cliConfig", cli_config.as_map()))
        if runid:
            args.append(SetuArg.arg("runId", runid))

        response = self._send_request(
            ArjunaComponent.TEST_SESSION,
            TestSessionActionType.INIT,
            *args
        )
        self._set_setu_id(response.get_value_for_testsession_setu_id())
        self._set_self_setu_id_arg("testSessionSetuId")
        return self.__create_config_from_response(response)

    def __create_config_from_response(self, response, name=None):
        res_data = response.get_data()
        config = DefaultTestConfig(
            self,
            name and name or self.__DEF_CONF_NAME,
            response.get_value_for_config_setu_id(),
            res_data["arjunaOptions"],
            res_data["userOptions"]
        )
        return config

    def finish(self):
        pass
        # To do

    def __register_config(self, name, hasParent, parentConfigId, arjunaOptions, userOptions):
        response = self._send_request(
                ArjunaComponent.CONFIGURATOR,
                ConfigActionType.REGISTER_NEW_CONFIG,
                SetuArg.arg("hasParent", hasParent),
                SetuArg.arg("parentConfigId", parentConfigId),
                SetuArg.arg("arjunaOptions", arjunaOptions),
                SetuArg.arg("userOptions", userOptions)
        )
        return self.__create_config_from_response(response, name)

    def register_config(self, name, arjuna_options, user_options):
        return self.__register_config(name, False, None, arjuna_options, user_options)

    def register_child_config(self, name, parent_conf_id, arjuna_options, user_options):
        return self.__register_config(name, True, parent_conf_id, arjuna_options, user_options)

    def create_file_data_source(self, record_type, file_name, *arg_pairs):
        response = self._send_request(
            ArjunaComponent.DATA_SOURCE,
            DataSourceActionType.CREATE_FILE_DATA_SOURCE,
            *arg_pairs
        )
        return response.get_data_source_id()

    def create_gui(self, automator, *setu_args):
        args = setu_args + (SetuArg.arg("automatorSetuId", automator.get_setu_id()), )
        response = self._send_request(
            ArjunaComponent.GUI,
            GuiActionType.CREATE_GUI,
            *args
        )
        return response.get_gui_setu_id()





