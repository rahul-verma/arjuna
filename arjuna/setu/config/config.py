import platform
import os
from enum import Enum
from arjuna.tpi.enums import *

from arjuna.setu.types import SetuManagedObject
from arjuna.lib.types.descriptors import *


class Config(SetuManagedObject):
    DESKTOP_CONTEXTS = {GuiAutomationContext.NATIVE, GuiAutomationContext.WEB}
    MOBILE_WEB_CONTEXTS = {GuiAutomationContext.ANDROID_WEB, GuiAutomationContext.IOS_WEB}
    ALL_WEB_CONTEXTS = {GuiAutomationContext.WEB, GuiAutomationContext.ANDROID_WEB, GuiAutomationContext.IOS_WEB}
    MOBILE_NATIVE_CONTEXTS = {GuiAutomationContext.ANDROID_NATIVE, GuiAutomationContext.IOS_NATIVE}

    def __init__(self):
        super().__init__()
        self.__setu_config = None
        self.__user_config = None
        self.__processor = None

    @property
    def setu_config(self):
        return self.__setu_config

    @setu_config.setter
    def setu_config(self, conf):
        self.__setu_config = conf

    @property
    def user_config(self):
        return self.__user_config

    @user_config.setter
    def user_config(self, conf):
        self.__user_config = conf

    @property
    def processor(self):
        return self.__processor

    @processor.setter
    def processor(self, processor):
        self.__processor = processor

    def as_json_dict(self):
        return {
            "arjunaOptions": self.__setu_config.as_json_dict(),
            "userOptions": self.__user_config.as_json_dict()
        }

    def __modify_bin_name_for_windows(self, name):
        if platform.system().lower() == "windows":
            return name + ".exe"
        else:
            return name

    def __get_driver_path(self, name):
        existing_driver_path = self.setu_config.value(ArjunaOption.SELENIUM_DRIVER_PATH)
        not_set_yet_str = "<DRIVER_NAME>"
        if existing_driver_path.find(not_set_yet_str) != -1:
            return self.setu_config.value(ArjunaOption.SELENIUM_DRIVER_PATH).replace(not_set_yet_str, self.__modify_bin_name_for_windows(name))
        else:
            # Some other driver might have been set
            return os.path.join(os.path.dirname(existing_driver_path), name)

    def process_arjuna_options(self):
        for_browser = {
            BrowserName.CHROME: {
                ArjunaOption.SELENIUM_DRIVER_PROP : "webdriver.chrome.driver",
                ArjunaOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("chromedriver")
            },

            BrowserName.FIREFOX: {
                ArjunaOption.SELENIUM_DRIVER_PROP : "webdriver.gecko.driver",
                ArjunaOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("geckodriver")
            },

            BrowserName.SAFARI: {
                ArjunaOption.SELENIUM_DRIVER_PROP : "webdriver.safari.driver",
                ArjunaOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("safaridriver")
            }
        }

        browser = self.setu_config.get_browser_name()
        for opt, opt_value in for_browser[browser].items():
            self.setu_config._config_dict[opt] = opt_value

    def update(self, override_config):
        self.setu_config.update(override_config.setu_config)
        self.user_config.update(override_config.user_config)


class AbstractConfig:

    def __init__(self, config_dict):
        self.__config_dict = config_dict

    @property
    def _config_dict(self):
        return self.__config_dict

    def is_not_set(self, key):
        self._validate_key(key)
        try:
            return self.value(key).upper() == "NOT_SET"
        except:
            return False

    def _validate_key(self, key):
        pass

    def __value(self, v):
        if isinstance(v, Enum):
            return v.name
        elif type(v) is list:
            out = []
            for value in v:
                if isinstance(value, Enum):
                    out.append(value.name)
                else:
                    out.append(value)
            return out
        else:
            return v

    def value(self, key):
        self._validate_key(key)
        v = self.__config_dict[key]
        return self.__value(v)

    def as_map(self):
        return self.__config_dict

    def __as_enum_name_or_same(self, input):
        if isinstance(input, Enum):
            return input.name
        else:
            return input

    def as_json_dict(self):
        return {k:self.__value(v) for k,v in self.as_map().items()}

    def update(self, override_config):
        self.__config_dict.update(override_config.as_map())

    def enumerate(self):
        from arjuna import ArjunaCore
        keys = list(self.central_config.arjuna_options.keys())
        keys.sort()
        ArjunaCore.console.marker(100)
        header = " Central Properties Table "
        mark_length = (50 - len(header)// 2)
        ArjunaCore.console.marker_on_same_line(mark_length)
        ArjunaCore.console.display_on_same_line(header)
        ArjunaCore.console.marker(mark_length)
        ArjunaCore.console.marker(100)
        for key in keys:
            if self.central_config.arjuna_options[key].visible:
                sval = self.central_config.arjuna_options[key].value
                if EnumConstant.check(sval):
                    sval = sval.name
                elif EnumConstantList.check(sval):
                    sval = str([i.name for i in sval])
                else:
                    if key != "arjuna.root.dir" and String.check(sval):
                        sval = sval.replace(ARJUNA_ROOT, "<arjuna_root_dir>")
                    else:
                        sval = str(sval)

                ArjunaCore.console.display(
                    "| {:60s}| {}".format(self.central_config.arjuna_options[key].text,
                                          sval))
                ArjunaCore.console.display("| {:60s}| {}".format("(" + key + ")", ""))
                ArjunaCore.console.marker(100)
        ArjunaCore.console.marker(100)


class UserConfig(AbstractConfig):

    def __init__(self, config_dict):
        super().__init__(config_dict)


class SetuConfig(AbstractConfig):

    def __init__(self, config_dict):
        super().__init__(config_dict)

    def _validate_key(self, key):
        if not isinstance(key, ArjunaOption):
            raise Exception("Key must be an enum consts of type ArjunaOption")

    def as_json_dict(self):
        out = {k.name: v for k,v in super().as_json_dict().items()}
        return out

    def get_gui_automator_name(self):
        return self._config_dict[ArjunaOption.AUTOMATOR_NAME]

    def get_guiauto_actor_mode(self):
        return self._config_dict[ArjunaOption.SETU_GUIAUTO_ACTOR_MODE]

    def get_guiauto_context(self):
        return self._config_dict[ArjunaOption.GUIAUTO_CONTEXT]

    def get_browser_name(self):
        return BrowserName[self.value(ArjunaOption.BROWSER_NAME)]

    def get_host_os(self):
        return DesktopOS[self.value(ArjunaOption.TESTRUN_HOST_OS)]

    def has_desktop_context(self):
        return self.get_guiauto_context() in Config.DESKTOP_CONTEXTS

    def has_mobile_web_context(self):
        return self.get_guiauto_context() in Config.MOBILE_WEB_CONTEXTS

    def has_mobile_native_context(self):
        return self.get_guiauto_context() in Config.MOBILE_NATIVE_CONTEXTS

    def has_web_context(self):
        return self.get_guiauto_context() in Config.ALL_WEB_CONTEXTS
