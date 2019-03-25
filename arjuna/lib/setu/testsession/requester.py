from arjuna.lib.setu.core.requester.config import DefaultTestConfig, SetuActionType, SetuArg
from arjuna.lib.setu.core.requester.connector import BaseSetuObject

class DefaultTestSession(BaseSetuObject):
    
    def __init__(self):
        super().__init__()
        self.__DEF_CONF_NAME = "central"

    def init(self, project_root_dir):
        super().__init__()
        response = self._send_request(SetuActionType.TESTSESSION_INIT, SetuArg.arg("projectRootDir", project_root_dir))
        self._set_setu_id(response.get_value_for_testsession_setu_id())
        self._set_self_setu_id_arg("testSessionSetuId")
        config = DefaultTestConfig(self, self.__DEF_CONF_NAME, response.get_value_for_config_setu_id())

        return config

    def finish(self):
        pass
        # To do

    def __register_config(self, hasParent, parentConfigId, setuOptions, userOptions):
        response = self._send_request(
                SetuActionType.TESTSESSION_REGISTER_CONFIG,
                SetuArg.arg("hasParent", hasParent),
                SetuArg.arg("parentConfigId", parentConfigId),
                SetuArg.arg("setuOptions", setuOptions),
                SetuArg.arg("userOptions", userOptions)
        )
        return response.getValueForConfigSetuId()

    def register_config(self, arjuna_options, user_options):
        return self.__register_config(False, None, arjuna_options, user_options)

    def register_child_config(self, parent_conf_id, arjuna_options, user_options):
        return self.__register_config(True, parent_conf_id, arjuna_options, user_options)

    def create_file_data_source(self, record_type, file_name, *arg_pairs):
        response = self._send_request(
            SetuActionType.TESTSESSION_CREATE_FILE_DATA_SOURCE,
            *arg_pairs
        )
        return response.getDataSourceSetuId()

    def create_gui(self, automator, *setu_args):
        args = setu_args + [SetuArg.arg("automatorSetuId", automator.get_setu_id())]
        response = self._send_request(
            SetuActionType.TESTSESSION_CREATE_GUI,
            *args
        )
        return response.get_gui_setu_id()





