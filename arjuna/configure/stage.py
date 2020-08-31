# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from arjuna.core.constant import ConfigStage
from arjuna.tpi.error import DisallowedArjunaOptionError

_RAW_OPTION_LEVELS = {

    ConfigStage.DEFAULT: {
        "ARJUNA_ROOT_DIR",
        "ARJUNA_EXTERNAL_IMPORTS_DIR",
        "LOG_NAME",
        "RUN_HOST_OS",
        "L10N_DIR",
        "PROJECT_NAME",
        "PROJECT_ROOT_DIR",
        "CONF_PROJECT_FILE",
        "TESTS_DIR",
        "HOOKS_DIR",
        "REPORTS_DIR",
        "REPORT_DIR",
        "REPORT_XML_DIR",
        "REPORT_HTML_DIR",
        "LOG_DIR",
        "SCREENSHOTS_DIR",
        "TOOLS_DIR",
        "TOOLS_BMPROXY_DIR",
        "TEMP_DIR",
        "CONF_DIR",
        "CONF_DATA_FILE",
        "CONF_ENVS_FILE",
        "CONF_SESSIONS_FILE",
        "CONF_STAGES_FILE",
        "CONF_GROUPS_FILE",
        "CONF_WITHX_FILE",
        "DATA_DIR",
        "DATA_SRC_DIR",
        "DATA_REF_DIR",
        "DATA_REF_CONTEXTUAL_DIR",
        "DATA_REF_INDEXED_DIR",
        "DATA_FILE_DIR",
        "GUIAUTO_NAME",
        "GUIAUTO_DIR",
        "GUIAUTO_NAMESPACE_DIR",
        "GUIAUTO_DEF_MULTICONTEXT",
        "GUIAUTO_CONTEXT",
        "SELENIUM_DRIVER_PROP",
        "SELENIUM_DRIVERS_DIR",
        "SELENIUM_DRIVER_PATH",
        "RUN_ID",
    },

    ConfigStage.CLI: {
        "RUN_SESSION_NAME",
        "LOG_FILE_LEVEL",
        "LOG_CONSOLE_LEVEL",
        "REPORT_FORMATS",
    },

    ConfigStage.REFERENCE: {
        "LOG_ALLOWED_CONTEXTS",
        "REPORT_SCREENSHOTS_ALWAYS",
        "REPORT_NETWORK_ALWAYS",
        "L10N_LOCALE",
        "L10N_STRICT",
        "BROWSER_NETWORK_RECORDER_ENABLED",
        "DEPS_DIR"
    },

    ConfigStage.CODED: {
        "REPORT_NETWORK_FILTER",
        "APP_URL",
        "BROWSER_NAME",
        "BROWSER_HEADLESS",
        "BROWSER_VERSION",
        "BROWSER_MAXIMIZE",
        "BROWSER_DIM_HEIGHT",
        "BROWSER_DIM_WIDTH",
        "BROWSER_BIN_PATH",
        "BROWSER_NETWORK_RECORDER_AUTOMATIC",
        "SCROLL_PIXELS",
        "GUIAUTO_MAX_WAIT",
        "GUIAUTO_SLOMO_ON",
        "GUIAUTO_SLOMO_INTERVAL",
        "MOBILE_OS_NAME",
        "MOBILE_OS_VERSION",
        "MOBILE_DEVICE_NAME",
        "MOBILE_DEVICE_UDID",
        "MOBILE_APP_FILE_PATH",
        "SELENIUM_DRIVER_DOWNLOAD",
        "SELENIUM_SERVICE_URL",
        "APPIUM_SERVICE_URL",
        "APPIUM_AUTO_LAUNCH",
        "IMG_COMP_MIN_SCORE"
        }
    }


class ConfigStageKeys:

    __OPTION_LEVELS = {
        ConfigStage.CODED: _RAW_OPTION_LEVELS[ConfigStage.CODED],
        ConfigStage.REFERENCE: _RAW_OPTION_LEVELS[ConfigStage.CODED].union(_RAW_OPTION_LEVELS[ConfigStage.REFERENCE]),
        ConfigStage.CLI: _RAW_OPTION_LEVELS[ConfigStage.CODED].union(_RAW_OPTION_LEVELS[ConfigStage.REFERENCE]).union(_RAW_OPTION_LEVELS[ConfigStage.CLI]),
        ConfigStage.DEFAULT: _RAW_OPTION_LEVELS[ConfigStage.CODED].union(_RAW_OPTION_LEVELS[ConfigStage.REFERENCE]).union(_RAW_OPTION_LEVELS[ConfigStage.CLI]).union(_RAW_OPTION_LEVELS[ConfigStage.CLI])
    }

    @classmethod
    def validate(cls, stage, option):
        if option not in cls.__OPTION_LEVELS[stage]:
            raise DisallowedArjunaOptionError(stage, option)
