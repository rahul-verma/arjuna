from enum import Enum, auto

from arjuna.lib.setu.core.webclient.requester import SetuAgentRequester


class ResponseCode:
    SUCCESS = auto()
    ERROR = auto()


class DefaultSetuResponse:

    def __init__(self, json_dict):
        self.__response_dict = json_dict

    def getResult(self):
        return ResponseCode[self.__response_dict["result"].upper()]

    def getMessage(self):
        return self.__response_dict["emessage"]

    def getTrace(self):
        return self.__response_dict["etrace"]

    def getData(self):
        return self.__response_dict["responseData"]

    def getValueForKey(self, keyName):
        return self.getData()[keyName]

    def getValue(self):
        return self.getValueForKey("value")

    def getValueForValueAttr(self):
        return self.getValueForKey("value")

    def getValueForText(self):
        return self.getValueForKey("text")

    def getValueForCheckResult(self):
        return self.getValueForKey("checkResult")

    def getValueForElementSetuId(self):
        return self.getValueForKey("elementSetuId")

    def getValueForTestSessionSetuId(self):
        return self.getValueForKey("testSessionSetuId")

    def getValueForConfigSetuId(self):
        return self.getValueForKey("configSetuId")

    def getValueForGuiAutomatorSetuId(self):
        return self.getValueForKey("automatorSetuId")

    def getGuiSetuId(self):
        return self.getValueForKey("guiSetuId")

    def getDataSourceSetuId(self):
        return self.getValueForKey("dataSourceSetuId")

    def addDataItem(self, name, value):
        if not self.getData():
            self.__response_dict["responseData"] = {}
        self.__response_dict["responseData"][name] = value


class _DefaultSetuRequester:
    def __init__(self):
        self.__setu_url = "http://localhost:9000"
        self.__base_uri = "/setu"
        self.__rest_client = SetuAgentRequester(self.__setu_url)

    def post(self, request):
        return DefaultSetuResponse(self.__rest_client.post(self.__base_uri, request.as_json()))


class _DefaultSetuRequest:

    def __init__(self, setu_action_type):
        self.__request_body = dict()
        self.__request_body["action"] = setu_action_type.name
        self.__request_body["args"] = dict()

    def add_arg(self, name, value):
        self.__request_body[name] = value

    def add_all_args(self, arg_dict):
        self.__request_body["args"].update(arg_dict)

    def as_json(self):
        return self.__request_body


class BaseSetuObject:
    SETU_CLIENT = _DefaultSetuRequester()

    def __init__(self):
        self.__setu_id = None
        self.__core_args = dict()

    def getSetuId(self):
        return self.__setu_id

    def _set_setu_id(self, id):
        self.__setu_id = id

    def _set_test_session_setu_id_arg(self, id):
        self.__core_args["testSessionSetuId"] = id

    def _set_automator_setu_id_arg(self, id):
        self.__core_args["automatorSetuId"] = id

    def _set_gui_setu_id_arg(self, id):
        self.__core_args["guiSetuId"] = id

    def _set_self_setu_id_arg(self, id_name):
        self.__core_args[id_name] = self.getSetuId()

    def _add_args(self, *vargs):
        for arg in vargs:
            self.__core_args[arg.getName()] = arg.getObject()

    def __prepare_request_with_core_args(self, request):
        for name, value in self.__core_args.items():
            request.addArg(name, value)

    def __prepare_request(self, request, *vargs):
        for arg in vargs:
            request.addArg(arg.getName(), arg.getObject())

    def _create_request(self, setu_action_type, *vargs):
        request = _DefaultSetuRequest(setu_action_type)
        self.__prepare_request_with_core_args(request)
        self.__prepare_request(request, *vargs)
        return request

    def _send_request(self, setu_action_type, *vargs):
        request = self._create_request(setu_action_type, *vargs)
        return self.SETU_CLIENT.post(request)

class SetuArg:

    def __init__(self, name, obj):
        self.__name = name
        self.__obj = obj

    def getName(self):
        return self.__name

    def getObject(self):
        return self.__obj

    @staticmethod
    def arg(name, obj):
        return SetuArg(name, obj)

    @staticmethod
    def textArg(name, obj):
        return SetuArg("text", obj)

    @staticmethod
    def valueArg(name, obj):
        return SetuArg("value", obj)

    @staticmethod
    def indexArg(name, obj):
        return SetuArg("index", obj)

    @staticmethod
    def configArg(name, obj):
        return SetuArg("configSetuId", obj)

    @staticmethod
    def arg(name, obj):
        return SetuArg(name, obj)

