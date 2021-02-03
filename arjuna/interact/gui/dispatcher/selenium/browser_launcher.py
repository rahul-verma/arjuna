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


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *


class BrowserLauncher:

    @classmethod
    def launch(cls, config, svc_url=None, proxy=None):
        driver_path = config["arjuna_options"]["SELENIUM_DRIVER_PATH"]
        browser_bin_path = config["arjuna_options"]["BROWSER_BIN_PATH"]
        browser_name = config["arjuna_options"]["BROWSER_NAME"]
        return CREATOR_MAP[browser_name.name](config, driver_path, browser_bin_path, svc_url, proxy=proxy)

    @classmethod
    def are_browser_prefs_set(cls, config):
        return "browserPreferences" in config and config["browserPreferences"]

    @classmethod
    def are_browser_args_set(cls, config):
        return "browserArgs" in config and config["browserArgs"]

    @classmethod
    def are_extensions_set(cls, config):
        return "browserExtensions" in config and config["browserExtensions"]

    @classmethod
    def _create_chrome(cls, config, driver_path, browser_bin_path, svc_url, proxy=None):
        from selenium.webdriver import Chrome, ChromeOptions

        caps = DesiredCapabilities.CHROME
        caps.update(config["driverCapabilities"])

        # if config["arjuna_options"]["BROWSER_PROXY_ON"]:
        #     proxy = Proxy()
        #     proxy_string = "{}.{}".format(
        #         config["arjuna_options"]["BROWSER_PROXY_HOST"],
        #         config["arjuna_options"]["BROWSER_PROXY_PORT"]
        #     )
        #     proxy.http_proxy = proxy_string
        #     proxy.ssl_proxy = proxy_string
        #     proxy.add_to_capabilities(caps)

        from arjuna import log_debug
        log_debug("Is proxy set for Chrome?: {}".format(proxy is not None))
        if proxy is not None:
            proxy.add_to_capabilities(caps)
            caps['acceptInsecureCerts'] = True

        options = ChromeOptions()

        if browser_bin_path.lower() != "not_set":
            options.binary_location = browser_bin_path

        if cls.are_browser_prefs_set(config):
            options.add_experimental_option("prefs", config["browserPreferences"])

        if config["arjuna_options"]["BROWSER_HEADLESS"]:
            options.add_argument("--headless")

        if cls.are_browser_args_set(config):
            for arg in config["browserArgs"]:
                options.add_argument(arg)

        if cls.are_extensions_set(config):
            for ext in config["browserExtensions"]:
                options.add_extension(ext)

        caps[ChromeOptions.KEY] = options.to_capabilities()[ChromeOptions.KEY]
        from selenium import webdriver
        return webdriver.Remote(svc_url, caps)

    @classmethod
    def _create_firefox(cls, config, driver_path, browser_bin_path, svc_url, proxy=None):
        from selenium.webdriver import Firefox
        from selenium.webdriver import FirefoxOptions
        from selenium.webdriver import FirefoxProfile

        profile = FirefoxProfile()
        # if config["arjuna_options"]["BROWSER_PROXY_ON"]:
        #     proxy = Proxy()
        #     proxy_string = "{}.{}".format(
        #         config["arjuna_options"]["BROWSER_PROXY_HOST"],
        #         config["arjuna_options"]["BROWSER_PROXY_PORT"]
        #     )
        #     proxy.http_proxy = proxy_string
        #     proxy.ssl_proxy = proxy_string
        #     profile.set_proxy(proxy)

        caps = DesiredCapabilities.FIREFOX
        caps.update(config["driverCapabilities"])

        from arjuna import log_debug
        log_debug("Is proxy set for Firefox?: {}".format(proxy is not None))
        if proxy is not None:
            proxy.add_to_capabilities(caps)
            caps['acceptInsecureCerts'] = True

        options = FirefoxOptions()

        if browser_bin_path.lower() != "not_set":
            options.binary_location = browser_bin_path

        if cls.are_browser_prefs_set(config):
            for pref, value in config["browserPreferences"].items():
                options.set_preference(pref, value)

        if config["arjuna_options"]["BROWSER_HEADLESS"]:
            options.add_argument("-headless")

        if cls.are_browser_args_set(config):
            for arg in config["browserArgs"]:
                options.add_argument(arg)

        from selenium import webdriver
        return webdriver.Remote(svc_url, browser_profile=profile, options=options)

        # driver = Firefox(executable_path=driver_path, firefox_profile=profile, capabilities=caps)
        # if cls.are_extensions_set(config):
        #     for ext in config["browserExtensions"]:
        #         driver.install_addon(ext)

        # return driver

    # @classmethod
    # def _create_safari(cls, config, driver_path, browser_bin_path):
    #     from selenium.webdriver import Safari

    #     caps = DesiredCapabilities.SAFARI
    #     caps.update(config["driverCapabilities"])

    #     return Safari(executable_path=driver_path, desired_capabilities=caps)


CREATOR_MAP = {
    "FIREFOX" : BrowserLauncher._create_firefox,
    "CHROME" : BrowserLauncher._create_chrome,
    # "SAFARI" : BrowserLauncher._create_safari,
}
