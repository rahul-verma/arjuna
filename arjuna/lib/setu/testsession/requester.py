from arjuna.tpi import Arjuna
from arjuna.lib.setu.core.requester.config import BaseTestConfig, SetuActionType, SetuArg
from arjuna.lib.setu.core.requester.connector import BaseSetuObject


class BaseTestSession(BaseSetuObject):
    
    def __init__(self):
        super().__init__()

    def init(self, root_dir):
        response = self._send_request(SetuActionType.TESTSESSION_INIT, SetuArg.arg("rootDir", root_dir))
        self.setSetuId(response.getValueForTestSessionSetuId())
        self.setSelfSetuIdArg("testSessionSetuId")
        config = BaseTestConfig(self, Arjuna.DEF_CONF_NAME, response.getValueForConfigSetuId())
        self.setSetuId(response.getValueForTestSessionSetuId())

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

    def registerConfig(self, setuOptions, userOptions):
        return self.__register_config(False, None, setuOptions, userOptions)

    def registerChildConfig(self, parentConfigId, setuOptions, userOptions):
        return self.__register_config(True, parentConfigId, setuOptions, userOptions)

    def createFileDataSource(self, recordType, fileName, argPairs):
        response = self._send_request(
            SetuActionType.TESTSESSION_CREATE_FILE_DATA_SOURCE,
            *argPairs
        )
        return response.getDataSourceSetuId()

    def createGui(self, automator, *setuArgs):
        args = setuArgs + [SetuArg.arg("automatorSetuId", automator.getSetuId())]
        response = self._send_request(
            SetuActionType.TESTSESSION_CREATE_GUI,
            *args
        )
        return response.getGuiSetuId()





