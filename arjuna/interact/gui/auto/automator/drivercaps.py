# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna.tpi.constant import *
from arjuna.core.constant import *
import pprint
from enum import Enum, auto

class SetuActorDriverConfigOption(Enum):
    GUIAUTO_NAME = auto()
    GUIAUTO_CONTEXT = auto()

    # Browser (Common)
    BROWSER_NAME = auto()
    BROWSER_HEADLESS = auto()
    BROWSER_BIN_PATH = auto()
    BROWSER_NETWORK_RECORDER_ENABLED = auto()
    TOOLS_BMPROXY_DIR = auto()
    # BROWSER_PROXY_ON = auto()
    # BROWSER_PROXY_HOST = auto()
    # BROWSER_PROXY_PORT = auto()
    MOBILE_OS_NAME = auto()

    # Selenium
    SELENIUM_DRIVER_PROP = auto()
    SELENIUM_DRIVER_PATH = auto()
    SELENIUM_DRIVER_DOWNLOAD = auto()
    SELENIUM_SERVICE_URL = auto()

    # Appium
    APPIUM_SERVICE_URL = auto()
    APPIUM_AUTO_LAUNCH = auto()

class DriverCapabilities:
    DRIVER_MAP = {
        "chrome": "chromedriver",
        "firefox": "geckodriver",
        "safari": "safaridriver"
    }

    # Selenium
    UNEXPECTED_ALERT_BEHAVIOUR = "unexpectedAlertBehaviour" # accept,dismiss,ignore
    UNHANDLED_PROMPT_BEHAVIOUR = "unhandledPromptBehavior" # accept,dismiss,ignore
    ELEMENT_SCROLL_BEHAVIOR = "elementScrollBehavior" #???
    AUTOMATION_NAME = "automationName"
    BROWSER_NAME = "browserName"
    BROWSER_VERSION = "browserVersion"

    # Appium
    PLATFORM_NAME = "platformName"
    PLATFORM_VERSION = "platformVersion"
    DEVICE_NAME = "deviceName"
    APP_PATH = "app"
    DEVICE_UDID = "udid"
    NEW_COMMAND_TIMEOUT = "newCommandTimeout" # unit: seconds
    AUTO_WEBVIEW = "autoWebview" # Default false
    NO_RESET = "noReset" # Default false
    FULL_RESET = "fullReset"
    CLEAR_SYSTEM_FILES = "clearSystemFiles"

    # Android
    ANDROID_APP_ACTIVITY = "appActivity"
    ANDROID_APP_PACKAGE = "appPackage"
    ANDROID_WAIT_ACTIVITY = "appWaitActivity"
    ANDROID_WAIT_PACKAGE = "appWaitPackage"
    ANDROID_UNICODE_KEYBOARD = "unicodeKeyboard"
    ANDROID_RESET_KEYBOARD = "resetKeyboard"

    #ios
    IOS_BUNDLE_ID = "bundleId"
    IOS_AUTO_ACCEPT_ALERTS = "autoAcceptAlerts"

    def __init__(self, config, json_dict):
        self.__config = config
        self.__out_dict = {
            "arjuna_options" : {},
            "browserArgs": [],
            "driverCapabilities": {},
            "browserPreferences":{},
            "browserExtensions":[]
        }

        from arjuna import ArjunaOption
        insecure_ssl_cert_allowed = config.value(ArjunaOption.ALLOW_INSECURE_SSL_CERT)
        if insecure_ssl_cert_allowed:
            self.__out_dict["driverCapabilities"]["acceptInsecureCerts"] = True

        self.__process_config(config)
        self.__process(json_dict)
        self.__host_os = self.__config.value(ArjunaOption.RUN_HOST_OS).name.lower()
        aname = self.__config.value(ArjunaOption.GUIAUTO_NAME).name.lower()
        acontext = self.__config.value(ArjunaOption.GUIAUTO_CONTEXT).name.lower()
        mobile_platform = self.__config.value(ArjunaOption.MOBILE_OS_NAME).name.lower()

        if aname == "selenium":
            self.__process_for_selenium(json_dict)
        elif aname == "appium":
            self.__process_for_appium(json_dict)
            if mobile_platform.lower() == "android":
                self.__process_for_android(json_dict)
            elif mobile_platform.lower() == "ios":
                self.__process_for_ios(json_dict)

            if acontext.lower() == "mobile_web":
                if mobile_platform.lower() == "android":
                    self.__process_for_android_web(json_dict)
                elif mobile_platform.lower() == "ios":
                    self.__process_for_ios_web(json_dict)
            elif acontext.lower() == "mobile_native":
                if mobile_platform.lower() == "android":
                    self.__process_for_android_native(json_dict)
                elif mobile_platform.lower() == "ios":
                    self.__process_for_ios_native(json_dict)
            elif acontext.lower() == "mobile_hybrid":
                if mobile_platform.lower() == "android":
                    self.__process_for_android_hybrid(json_dict)
                elif mobile_platform.lower() == "ios":
                    self.__process_for_ios_hybrid(json_dict)
        
        if not self.__out_dict["browserArgs"]:
            del self.__out_dict["browserArgs"]
        if not self.__out_dict["driverCapabilities"]:
            del self.__out_dict["driverCapabilities"]
        if not self.__out_dict["browserPreferences"]:
            del self.__out_dict["browserPreferences"]
        if not self.__out_dict["browserExtensions"]:
            del self.__out_dict["browserExtensions"]

    @property
    def processed_config(self):
        return self.__out_dict

    @property
    def _config(self):
        return self.__config

    def __process_config(self, config):
        self.__out_dict["automationContext"] = config.value(ArjunaOption.GUIAUTO_CONTEXT).name.upper()
        temp_d = config.get_arjuna_options_as_map()
        for k,v in temp_d.items():
            k = k.upper()
            if k in SetuActorDriverConfigOption.__members__:
                self.__out_dict["arjuna_options"][k] = v

    def __process(self, dict_from_requester):
        self.__out_dict["driverCapabilities"][self.UNEXPECTED_ALERT_BEHAVIOUR] = "dismiss"
        self.__out_dict["driverCapabilities"][self.UNHANDLED_PROMPT_BEHAVIOUR] = "dismiss"
        if not dict_from_requester: return
        if "browserArgs" in dict_from_requester and dict_from_requester["browserArgs"]:
            self.__out_dict["browserArgs"].extend(dict_from_requester["browserArgs"])
        if "driverCapabilities" in dict_from_requester and dict_from_requester["driverCapabilities"]:
            self.__out_dict["driverCapabilities"].update(
                {i:j for i,j in dict_from_requester["driverCapabilities"].items() if j !="not_set"})
        if "browserPreferences" in dict_from_requester and dict_from_requester["browserPreferences"]:
            self.__out_dict["browserPreferences"] = dict_from_requester["browserPreferences"]
        if "browserExtensions" in dict_from_requester and dict_from_requester["browserExtensions"]:
            self.__out_dict["browserExtensions"].extend(dict_from_requester["browserExtensions"])

    def __modify_for_windows(self, in_name):
        if self.__host_os == DesktopOS.WINDOWS:
            return in_name + ".exe"
        else:
            return in_name

    def __process_for_selenium(self, in_dict):
        browser_name = self._config.value(ArjunaOption.BROWSER_NAME).name.lower()
        self.__out_dict["driverCapabilities"][self.BROWSER_NAME] = browser_name
        browser_version = self._config.value(ArjunaOption.BROWSER_VERSION)
        if browser_version != "not_set":
            self.__out_dict["driverCapabilities"][self.BROWSER_VERSION] = browser_version

    def __process_for_appium(self, dict_from_requester):
        mobile_os_name = self._config.value(ArjunaOption.MOBILE_OS_NAME).name.lower()
        if mobile_os_name.lower() == "android":
            self.__out_dict["driverCapabilities"][self.PLATFORM_NAME] = "Android"
        elif mobile_os_name.lower() == "ios":
            self.__out_dict["driverCapabilities"][self.PLATFORM_NAME] = "iOS"
        self.__out_dict["driverCapabilities"][self.NEW_COMMAND_TIMEOUT] = 300 # 5 minutes 
        self.__out_dict["driverCapabilities"][self.PLATFORM_VERSION] = self._config.value(ArjunaOption.MOBILE_OS_VERSION)
        self.__out_dict["driverCapabilities"][self.DEVICE_NAME] = self._config.value(ArjunaOption.MOBILE_DEVICE_NAME)
        self.__out_dict["driverCapabilities"][self.APP_PATH] = self._config.value(ArjunaOption.MOBILE_APP_FILE_PATH)
        self.__out_dict["driverCapabilities"][self.DEVICE_UDID] = self._config.value(ArjunaOption.MOBILE_DEVICE_UDID)

    def __process_for_android(self, dict_from_requester):
        self.__out_dict["driverCapabilities"][self.AUTOMATION_NAME] = "UiAutomator2"
        self.__out_dict["driverCapabilities"][self.ANDROID_UNICODE_KEYBOARD] = True
        self.__out_dict["driverCapabilities"][self.ANDROID_RESET_KEYBOARD] = True

    def __process_for_android_native(self, dict_from_requester):
        pass
        # self.__out_dict["driverCapabilities"][self.ANDROID_APP_ACTIVITY] = self._config.value(ArjunaOption.MOBILE_APP_PACKAGE).name
        # self.__out_dict["driverCapabilities"][self.ANDROID_APP_PACKAGE] = self._config.value(ArjunaOption.MOBILE_APP_ACTIVITY)
        # self.__out_dict["capabilites"][self.ANDROID_WAIT_ACTIVITY] = self._config.value(ArjunaOption.MOBILE_APP_ACTIVITY)
        # self.__out_dict["capabilites"][self.ANDROID_WAIT_PACKAGE] = self._config.value(ArjunaOption.MOBILE_APP_FILE_PATH)

    def __process_for_android_web(self, dict_from_requester):
        # Browser
        browser_name = self._config.get_browser_name().lower()
        if browser_name.lower() != "chrome":
            raise Exception("{} is not a valid browser for Android.".format(browser_name))
        self.__out_dict["capabilities"][self.BROWSER_NAME] = browser_name

    def __process_for_android_hybrid(self, dict_from_requester):
        pass

    def __process_for_ios(self, dict_from_requester):
        self.__out_dict["driverCapabilities"][self.AUTOMATION_NAME] = "XCUITest"
        self.__out_dict["driverCapabilities"][self.IOS_AUTO_ACCEPT_ALERTS] = True

    def __process_for_ios_native(self, dict_from_requester):
        pass

    def __process_for_ios_web(self, dict_from_requester):
                self.__out_dict["driverCapabilities"][self.BROWSER_NAME] = self._config.get_browser_name()

    def __process_for_ios_hybrid(self, dict_from_requester):
        pass



'''
	
#Common (WebDriver)
BROWSER_NAME = "browserName"
BROWSER_VERSION = "browserVersion"

#Appium
PLATFORM_NAME = "platformName"
PLATFORM_VERSION = "platformVersion"
DEVICE_NAME = "deviceName"
APP_PATH = "app"
DEVICE_UDID = "udid"

Android{
// Android Specific
ANDROID_APP_ACTIVITY = "appActivity"
ANDROID_APP_PACKAGE = "appPackage"
ANDROID_WAIT_ACTIVITY = "appWaitActivity"
ANDROID_WAIT_PACKAGE = "appWaitPackage"
}

IOS {

}
'''