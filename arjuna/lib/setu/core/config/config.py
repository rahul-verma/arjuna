import platform
import os
from enum import Enum
from arjuna.lib.setu.core.constants import *

from arjuna.lib.setu.core.lib.setu_types import SetuManagedObject

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
            "setuOptions" : self.__setu_config.as_json_dict(),
            "userOptions" : self.__user_config.as_json_dict()
        }

    def __modify_bin_name_for_windows(self, name):
        if platform.system().lower() == "windows":
            return "name" + ".exe"
        else:
            return name

    def __get_driver_path(self, name):
        return os.path.join(self.setu_config.value(SetuConfigOption.SELENIUM_DRIVERS_DIR), self.__modify_bin_name_for_windows(name))

    def process_setu_options(self):
        for_browser = {
            Browser.CHROME : {
                SetuConfigOption.SELENIUM_DRIVER_PROP : "webdriver.chrome.driver",
                SetuConfigOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("chromedriver")
            },

            Browser.FIREFOX : {
                SetuConfigOption.SELENIUM_DRIVER_PROP : "webdriver.gecko.driver",
                SetuConfigOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("geckodriver")
            },

            Browser.SAFARI : {
                SetuConfigOption.SELENIUM_DRIVER_PROP : "webdriver.safari.driver",
                SetuConfigOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("safaridriver")
            }
        }

        browser = self.setu_config.value(SetuConfigOption.BROWSER_NAME)
        for opt, opt_value in for_browser[browser].items():
            self.setu_config._config_dict[opt] = opt_value



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

    def value(self, key):
        self._validate_key(key)
        return self.__config_dict[key]

    def as_map(self):
        return self.__config_dict

    def __as_enum_name_or_same(self, input):
        if isinstance(input, Enum):
            return input.name
        else:
            return input

    def as_json_dict(self):
        return {k:self.__as_enum_name_or_same(v) for k,v in self.as_map().items()}

    def get_guiauto_context(self):
        return GuiAutomationContext[self.value(SetuConfigOption.GUIAUTO_CONTEXT).upper()]

    def has_desktop_context(self):
        return self.get_guiauto_context() in Config.DESKTOP_CONTEXTS

    def has_mobile_web_context(self):
        return self.get_guiauto_context() in Config.MOBILE_WEB_CONTEXTS

    def has_mobile_native_context(self):
        return self.get_guiauto_context() in Config.MOBILE_NATIVE_CONTEXTS

    def has_web_context(self):
        return self.get_guiauto_context() in Config.ALL_WEB_CONTEXTS

class UserConfig(AbstractConfig):

    def __init__(self, config_dict):
        super().__init__(config_dict)

class SetuConfig(AbstractConfig):

    def __init__(self, config_dict):
        super().__init__(config_dict)

    def _validate_key(self, key):
        if not isinstance(key, SetuConfigOption):
            raise Exception("Key must be an enum consts of type SetuConfigOption")

    def as_json_dict(self):
        out = {k.name: v for k,v in super().as_json_dict().items()}
        return out