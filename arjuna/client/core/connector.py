from enum import Enum, auto

from arjuna.setu.webclient.requester import SetuAgentRequester
from arjuna.lib.value import AnyRefValue


class ResponseCode(Enum):
    SUCCESS = auto()
    ERROR = auto()


class DefaultSetuResponse:

    def __init__(self, json_dict):
        self.__response_dict = json_dict

    def get_result(self):
        return ResponseCode[self.__response_dict["result"].upper()]

    def get_message(self):
        return self.__response_dict["emessage"]

    def get_trace(self):
        return self.__response_dict["etrace"]

    def get_data(self):
        return self.__response_dict["responseData"]

    def get_value_for_key(self, key):
        return AnyRefValue(self.get_data()[key])

    def get_value(self):
        return self.get_value_for_key("value")

    def get_value_for_value_attr(self):
        return self.get_value_for_key("value")

    def get_value_for_text(self):
        return self.get_value_for_key("text").as_string()

    def get_value_for_check_result(self):
        return self.get_value_for_key("checkResult")

    def get_value_for_element_setu_id(self):
        return self.get_value_for_key("elementSetuId").as_string()

    def get_value_for_testsession_setu_id(self):
        return self.get_value_for_key("testSessionSetuId").as_string()

    def get_value_for_config_setu_id(self):
        return self.get_value_for_key("configSetuId").as_string()

    def get_value_for_guiautomator_setu_id(self):
        return self.get_value_for_key("automatorSetuId").as_string()

    def get_gui_setu_id(self):
        return self.get_value_for_key("guiSetuId").as_string()

    def get_data_source_setu_id(self):
        return self.get_value_for_key("dataSourceSetuId").as_string()

    def add_data_item(self, name, value):
        if not self.get_data():
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

    def __init__(self, component, setu_action_type):
        self.__request_body = dict()
        self.__request_body["component"] = component.name
        self.__request_body["action"] = setu_action_type.name
        self.__request_body["args"] = dict()

    def add_arg(self, name, value):
        self.__request_body["args"][name] = value

    def add_all_args(self, arg_dict):
        self.__request_body["args"].update(arg_dict)

    def as_json(self):
        return self.__request_body


class BaseSetuObject:
    SETU_CLIENT = _DefaultSetuRequester()

    def __init__(self):
        self.__setu_id = None
        self.__core_args = dict()

    def get_setu_id(self):
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
        self.__core_args[id_name] = self.get_setu_id()

    def _add_args(self, *vargs):
        for arg in vargs:
            self.__core_args[arg.get_name()] = arg.get_object()

    def __prepare_request_with_core_args(self, request):
        for name, value in self.__core_args.items():
            request.add_arg(name, value)

    def __prepare_request(self, request, *vargs):
        for arg in vargs:
            request.add_arg(arg.get_name(), arg.get_object())

    def _create_request(self, component, setu_action_type, *vargs):
        request = _DefaultSetuRequest(component, setu_action_type)
        self.__prepare_request_with_core_args(request)
        self.__prepare_request(request, *vargs)
        return request

    def _send_request(self, component, setu_action_type, *vargs):
        request = self._create_request(component, setu_action_type, *vargs)
        return self.SETU_CLIENT.post(request)


class SetuArg:

    def __init__(self, name, obj):
        self.__name = name
        self.__obj = obj

    def get_name(self):
        return self.__name

    def get_object(self):
        return self.__obj

    @staticmethod
    def arg(name, obj):
        return SetuArg(name, obj)

    @staticmethod
    def text_arg(obj):
        return SetuArg("text", obj)

    @staticmethod
    def value_arg(obj):
        return SetuArg("value", obj)

    @staticmethod
    def index_arg(obj):
        return SetuArg("index", obj)

    @staticmethod
    def config_arg(obj):
        return SetuArg("configSetuId", obj)

    @staticmethod
    def arg(name, obj):
        return SetuArg(name, obj)

