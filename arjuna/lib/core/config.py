from arjuna.lib.core.value import AbstractValueMap, StringKeyValueMap
from arjuna.lib.setu.core.requester.config import SetuActionType
from arjuna.lib.setu.core.requester.connector import BaseSetuObject, SetuArg
from arjuna.tpi.enums import ArjunaOption
from arjuna.tpi.enums import GuiAutomationContext, BrowserName, GuiAutomatorName


class DefaultTestConfig(BaseSetuObject):

    def __init__(self, test_session, name, setu_id):
        super().__init__()
        self.__session = test_session
        self.__name = name

        self._set_setu_id(setu_id)
        self._set_self_setu_id_arg("configSetuId")
        self._set_test_session_setu_id_arg(self.__session.get_setu_id())

    def get_test_session(self):
        return self.__session

    def __fetch_config_option_value(self, setu_action_type, option_str):
        response = self._send_request(setu_action_type, SetuArg.arg("option", option_str))
        return response.get_value()

    @staticmethod
    def normalize_option_str(option_str):
        return option_str.upper().strip().replace(".", "_")

    @staticmethod
    def normalize_arjuna_option_str(option_str):
        return ArjunaOption[DefaultTestConfig.normalize_option_str(option_str)]

    def get_arjuna_option_value(self, option):
        setu_option = option
        if type(option) is str:
            setu_option = DefaultTestConfig.normalize_arjuna_option_str(option)
        return self.__fetch_config_option_value(SetuActionType.CONFIGURATOR_GET_ARJUNA_OPTION_VALUE, setu_option.name)

    def get_user_option_value(self, option):
        user_option = DefaultTestConfig.normalize_option_str(option)
        return self.__fetch_config_option_value(SetuActionType.CONFIGURATOR_GET_USER_OPTION_VALUE, user_option)

    def get_name(self):
        return self.__name

    def get_gui_auto_context(self):
        return self.get_arjuna_option_value(ArjunaOption.GUIAUTO_CONTEXT).as_enum(GuiAutomationContext)

    def get_browser_type(self):
        return self.get_arjuna_option_value(ArjunaOption.BROWSER_NAME).as_enum(BrowserName)

    def get_browser_version(self):
        return self.get_arjuna_option_value(ArjunaOption.BROWSER_VERSION).as_string()

    def get_browser_binary_path(self):
        return self.get_arjuna_option_value(ArjunaOption.BROWSER_BIN_PATH).as_string()

    def get_test_run_env_name(self):
        return self.get_arjuna_option_value(ArjunaOption.TESTRUN_ENVIRONMENT).as_string()

    def get_screenshots_dir(self):
        return self.get_arjuna_option_value(ArjunaOption.SCREENSHOTS_DIR).as_string()

    def get_log_dir(self):
        return self.get_arjuna_option_value(ArjunaOption.LOG_DIR).as_string()

    def get_gui_auto_max_wait_time(self):
        return self.get_arjuna_option_value(ArjunaOption.GUIAUTO_MAX_WAIT).as_int()


class ArjunaOptionContainer(AbstractValueMap):

    def __init__(self, object_map=None, headers=None, objects=None):
        super().__init__(object_map, headers, objects)

    def _format_key_as_str(self, key):
        return str(key)


class ConfigContainer:

    def __init__(self):
        self.__arjuna_options = ArjunaOptionContainer()
        self.__user_options = StringKeyValueMap()

    @property
    def arjuna_options(self):
        return self.__arjuna_options

    @property
    def user_options(self):
        return self.__user_options

    def set_arjuna_option(self, arjuna_option, obj):
        if isinstance(arjuna_option, ArjunaOption):
            self.__arjuna_options.add_object(arjuna_option.name, obj)
        else:
            normalized_option = DefaultTestConfig.normalize_option_str(arjuna_option)
            self.__arjuna_options.add_object(ArjunaOption[normalized_option], obj)
        return self

    def set_user_option(self, option, obj):
        self.__user_options.add_object(DefaultTestConfig.normalize_option_str(option), obj)
        return self

    def set_option(self, option, obj):
        normalized_option = DefaultTestConfig.normalize_option_str(option)
        try:
            arj_option = ArjunaOption[normalized_option]
            self.set_arjuna_option(arj_option, obj)
        except:
            self.set_user_option(option, obj)
        return self

    def add_options(self, options):
        for option, obj in options.items():
            self.set_option(option, obj)
        return self

    def is_empty(self):
        if not self.arjuna_options and not self.user_options:
            return True
        return False


class _ConfigBuilder:

    def __init__(self, test_session, config_dict, conf_trace, code_mode):
        self.__code_mode = code_mode
        self.__test_session = test_session
        self.__config_dict = config_dict
        self.__conf_trace = conf_trace
        if "default_config" in config_dict:
            self.__parent_config_setu_id =  config_dict["default_config"].get_setu_id()
        else:
            self.__parent_config_setu_id = None
        self.__config_container = ConfigContainer()

    def parent_config(self, config):
        self.__parent_config_setu_id = config.get_setu_id()

    def selenium(self):
        self.__config_container.set_arjuna_option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.SELENIUM.name)
        return self

    def set_arjuna_option(self, option, obj):
        self.__config_container.set_arjuna_option(option, obj)

    def appium(self, context):
        self.set_arjuna_option(ArjunaOption.GUIAUTO_AUTOMATOR_NAME, GuiAutomatorName.APPIUM.name)
        self.set_arjuna_option(ArjunaOption.GUIAUTO_CONTEXT, context)
        return self

    def chrome(self):
        self.set_arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.CHROME.name)
        return self

    def firefox(self):
        self.set_arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX.name)
        return self

    def headless_mode(self):
        self.set_arjuna_option(ArjunaOption.BROWSER_HEADLESS_MODE, True)
        return self

    def guiauto_max_wait_time(self, seconds):
        self.set_arjuna_option(ArjunaOption.GUIAUTO_MAX_WAIT, seconds)
        return self

    def app(self, path):
        self.set_arjuna_option(ArjunaOption.MOBILE_APP_FILE_PATH, path)
        return self

    def mobile_device_name(self, name):
        self.set_arjuna_option(ArjunaOption.MOBILE_DEVICE_NAME, name)
        return self

    def mobile_device_udid(self, udid):
        self.set_arjuna_option(ArjunaOption.MOBILE_DEVICE_UDID, udid)
        return self

    def build(self, config_name="default_config"):
        config_setu_id = None
        if not self.__parent_config_setu_id:
            config_setu_id = self.__test_session.register_config(
                self.__config_container.arjuna_options.str_items(),
                self.__config_container.user_options.items())
        else:
            config_setu_id = self.__test_session.register_child_config(
                self.__parent_config_setu_id,
                self.__config_container.arjuna_options.str_items(),
                self.__config_container.user_options.items()
            )
        config = DefaultTestConfig(self.__test_session, config_name, config_setu_id)
        self.__config_dict[config_name] = config
        if self.__code_mode:
            if config_name not in self.__conf_trace:
                self.__conf_trace[config_name] = {"arjuna_options": set(), "user_options" : set()}
            self.__conf_trace[config_name]["arjuna_options"].update(self.__config_container.arjuna_options.items().keys())
            self.__conf_trace[config_name]["user_options"].update(self.__config_container.user_options.items().keys())


class DefaultTestContext:

    def __init__(self, test_session, name, parent_config=None):
        self.__parent_config_setu_id = parent_config and parent_config.get_setu_id() or None
        self.__test_session = test_session
        self.__name = name
        self.__configs = dict()
        self.__conf_trace = dict()

    def ConfigBuilder(self, code_mode=True):
        return _ConfigBuilder(self.__test_session, self.__configs, self.__conf_trace, code_mode)

    def update_with_file_config_container(self, container):
        for config_name, conf in self.__configs.items():
            builder = _ConfigBuilder(self.__test_session, self.__configs, self.__conf_trace, code_mode=False)
            builder.parent_config(conf)
            amap = container.arjuna_options
            umap = container.user_options
            if config_name in self.__conf_trace:
                if "arjuna_options" in self.__conf_trace[config_name]:
                    for k,v in container.arjuna_options.items():
                        if k not in self.__conf_trace[config_name]["arjuna_options"]:
                            builder.set_arjuna_option(k,v)
                else:
                    for k, v in container.arjuna_options.items():
                        builder.set_arjuna_option(k, v)
                if "user_options" in self.__conf_trace[config_name]:
                    for k,v in container.user_options.items():
                        if k not in self.__conf_trace[config_name]["user_options"]:
                            builder.set_user_option(k,v)
                else:
                    for k, v in container.user_options.items():
                        builder.set_user_option(k, v)
            else:
                print(type(container.arjuna_options.items()))
                for k in amap.keys():
                    builder.set_arjuna_option(k, amap.object(k))
                for k in umap.keys():
                        builder.set_user_option(k, umap.object(k))
            builder.build(config_name=config_name)

    def get_config(self, config_name="default_config"):
        return self.__configs[config_name]

    def _add_configs(self, configs):
        self.__configs.update(configs)

    def _add_conf_trace(self, conf_trace):
        self.__conf_trace.update(conf_trace)

    def _get_conf_trace(self):
        return self.__conf_trace

    def _get_configs(self):
        return self.__configs

    def _get_test_session(self):
        return self.__test_session

    def get_name(self):
        return self.__name


class InternalTestContext(DefaultTestContext):

    def __init__(self, test_session, name, parent_config=None):
        super().__init__(test_session, name, parent_config)

    def add_config(self, config):
        self.__configs[config.get_name()] = config

    def clone(self):
        out_context = InternalTestContext(self._get_test_session(), self.get_name())
        out_context._add_configs(self._get_configs())
        out_context._add_conf_trace(self._get_conf_trace())
        return out_context

    def clone_for_user(self):
        out_context = DefaultTestContext(self._get_test_session(), self.get_name())
        out_context._add_configs(self._get_configs())
        out_context._add_conf_trace(self._get_conf_trace())
        return out_context

    def update_from_context(self, context):
        self._add_configs(context._get_configs())


class CliArgsConfig:

    def __init__(self, arg_dict):
        self.__aco = {}
        self.__ato = {}
        self.__uco = {}
        self.__uto = {}

        kinds = {
            "aco": self.__aco,
            "ato": self.__ato,
            "uco": self.__uco,
            "uto": self.__uto
        }

        lower_actual_key_map = {i.lower():i for i in arg_dict}
        for kind in kinds:
            if kind in lower_actual_key_map:
                actual_key = lower_actual_key_map[kind]
                d_item = arg_dict[actual_key]
                if d_item:
                    for entry in d_item:
                        k,v = entry
                        kinds[kind][k.lower()] = v
                del arg_dict[actual_key]

        for akey, avalue in arg_dict.items():
            self.__aco[akey.lower()] = avalue

    def as_map(self):
        return {
            "arjunaCentralOptions": self.__aco,
            "arjunaTestOptions": self.__ato,
            "userCentralOptions": self.__uco,
            "userTestOptions": self.__uto
        }