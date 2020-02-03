'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from enum import Enum, auto

class ArjunaOption(Enum):
    ARJUNA_ROOT_DIR = auto()
    ARJUNA_EXTERNAL_TOOLS_DIR = auto()
    ARJUNA_EXTERNAL_IMPORTS_DIR = auto()
    PYTHON_LOG_NAME = auto()
    LOG_NAME = auto()

    RUN_ID = auto()

    LOG_FILE_LEVEL = auto()
    LOG_CONSOLE_LEVEL = auto()

    PROJECT_NAME = auto()
    PROJECT_ROOT_DIR = auto()
    PROJECT_CONF_FILE = auto()
    PROJECT_TESTS_DIR = auto()
    PROJECT_REPORT_DIR = auto()
    PROJECT_REPORT_FORMATS = auto()
    PROJECT_RUN_REPORT_DIR = auto()
    PROJECT_RUN_REPORT_XML_DIR = auto()
    PROJECT_RUN_REPORT_HTML_DIR = auto()
    PROJECT_RUN_LOG_DIR = auto()
    PROJECT_RUN_SCREENSHOTS_DIR = auto()

    DATA_DIR = auto()
    DATA_SOURCES_DIR = auto()
    DATA_REFERENCES_DIR = auto()
    SCREENSHOTS_DIR = auto()
    CONFIG_DIR = auto()

    SETU_PROJECT_DIRS_FILES = auto()
    REPORT_DIR = auto()
    ARCHIVES_DIR = auto()

    AUT_BASE_URL = auto()

    TESTRUN_ENVIRONMENT = auto()
    TESTRUN_HOST_OS = auto()

    SETU_GUIAUTO_ACTOR_MODE = auto()
    SETU_GUIAUTO_ACTOR_URL = auto()

    AUTOMATOR_NAME = auto()

    BROWSER_NAME = auto()
    BROWSER_VERSION = auto()
    BROWSER_MAXIMIZE = auto()
    BROWSER_DIM_HEIGHT = auto()
    BROWSER_DIM_WIDTH = auto()
    BROWSER_BIN_PATH = auto()
    BROWSER_PROXY_ON = auto()

    GUIAUTO_INPUT_DIR = auto()
    GUIAUTO_NAMESPACE_DIR = auto()
    GUIAUTO_DEF_MULTICONTEXT = auto()
    GUIAUTO_CONTEXT = auto()
    SCROLL_PIXELS = auto()
    SWIPE_TOP = auto()
    SWIPE_BOTTOM = auto()
    SWIPE_MAX_WAIT = auto()
    GUIAUTO_MAX_WAIT = auto()
    GUIAUTO_SLOMO_ON = auto()
    GUIAUTO_SLOMO_INTERVAL = auto()

    MOBILE_OS_NAME = auto()
    MOBILE_OS_VERSION = auto()
    MOBILE_DEVICE_NAME = auto()
    MOBILE_DEVICE_UDID = auto()
    MOBILE_APP_FILE_PATH = auto()

    SELENIUM_DRIVER_PROP = auto()
    SELENIUM_DRIVERS_DIR = auto()
    SELENIUM_DRIVER_PATH = auto()

    APPIUM_HUB_URL = auto()
    APPIUM_AUTO_LAUNCH = auto()

    IMAGE_COMPARISON_MIN_SCORE = auto()

    UNITEE_PROJECT_DIRS_FILES = auto()
    UNITEE_PROJECT_SESSIONS_DIR = auto()
    UNITEE_PROJECT_GROUPS_DIR = auto()
    UNITEE_PROJECT_TESTS_DIR = auto()
    UNITEE_PROJECT_TEST_MODULE_IMPORT_PREFIX = auto()
    UNITEE_PROJECT_FIXTURES_IMPORT_PREFIX = auto()
    UNITEE_PROJECT_CORE_DIR = auto()
    UNITEE_PROJECT_CORE_DB_CENTRAL_DIR = auto()
    UNITEE_PROJECT_CORE_DB_CENTRAL_DBFILE = auto()
    UNITEE_PROJECT_CORE_DB_RUN_DBFILE = auto()
    UNITEE_PROJECT_CORE_DB_ALLRUN_DIR = auto()
    UNITEE_PROJECT_CORE_DB_TEMPLATE_DIR = auto()
    UNITEE_PROJECT_CORE_DB_TEMPLATE_CENTRAL_DBFILE = auto()
    UNITEE_PROJECT_CORE_DB_TEMPLATE_RUN_DBFILE = auto()
    UNITEE_PROJECT_REPORTER_MODE = auto()
    UNITEE_PROJECT_ACTIVE_REPORTERS = auto()
    UNITEE_PROJECT_DEFERRED_REPORTERS = auto()
    UNITEE_PROJECT_FAILFAST = auto()
    UNITEE_PROJECT_REPORT_NAME_FORMAT = auto()
    UNITEE_PROJECT_REPORT_HEADERS_TMETA = auto()
    UNITEE_PROJECT_REPORT_HEADERS_IGMETA = auto()
    UNITEE_PROJECT_REPORT_HEADERS_PROPS = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_TEST = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_STEP = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_ISSUE = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_IGNORED = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_FIXTURE = auto()
    UNITEE_PROJECT_REPORT_HEADERS_REPORTABLE_EVENT = auto()
    UNITEE_PROJECT_RUNID = auto()
    UNITEE_PROJECT_IRUNID = auto()
    UNITEE_PROJECT_SESSION_NAME = auto()
    UNITEE_PROJECT_CORE = auto()
    UNITEE_PROJECT_SCREENSHOTS_RUN_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JDB_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_TESTS_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_IGNOREDTESTS_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_ISSUES_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_EVENTS_DIR = auto()
    UNITEE_PROJECT_RUN_REPORT_JSON_FIXTURES_DIR = auto()


class Key(Enum):
	NULL = auto()
	CANCEL = auto()
	HELP = auto()
	BACKSPACE = auto()
	BACK_SPACE = auto()
	TAB = auto()
	CLEAR = auto()
	RETURN = auto()
	ENTER = auto()
	SHIFT = auto()
	LEFT_SHIFT = auto()
	CONTROL = auto()
	LEFT_CONTROL = auto()
	ALT = auto()
	LEFT_ALT = auto()
	PAUSE = auto()
	ESCAPE = auto()
	SPACE = auto()
	PAGE_UP = auto()
	PAGE_DOWN = auto()
	END = auto()
	HOME = auto()
	LEFT = auto()
	ARROW_LEFT = auto()
	UP = auto()
	ARROW_UP = auto()
	RIGHT = auto()
	ARROW_RIGHT = auto()
	DOWN = auto()
	ARROW_DOWN = auto()
	INSERT = auto()
	DELETE = auto()
	SEMICOLON = auto()
	EQUALS = auto()

	NUMPAD0 = auto()
	NUMPAD1 = auto()
	NUMPAD2 = auto()
	NUMPAD3 = auto()
	NUMPAD4 = auto()
	NUMPAD5 = auto()
	NUMPAD6 = auto()
	NUMPAD7 = auto()
	NUMPAD8 = auto()
	NUMPAD9 = auto()
	MULTIPLY = auto()
	ADD = auto()
	SEPARATOR = auto()
	SUBTRACT = auto()
	DECIMAL = auto()
	DIVIDE = auto()

	F1 = auto()
	F2 = auto()
	F3 = auto()
	F4 = auto()
	F5 = auto()
	F6 = auto()
	F7 = auto()
	F8 = auto()
	F9 = auto()
	F10 = auto()
	F11 = auto()
	F12 = auto()

	META = auto()
	COMMAND = auto()

class ModifierKey(Enum):
    CTRL = auto()
    CMD = auto()
    XCTRL = auto()
    ALT = auto()
    SHIFT = auto()

class TimeUnit(Enum):
    MILLI_SECONDS = auto()
    SECONDS = auto()
    MINUTES = auto()

class DesktopOS(Enum):
    WINDOWS = auto()
    MAC = auto()

class SetuActorMode(Enum):
    LOCAL = auto()
    REMOTE = auto()

class MobileOsName(Enum):
    ANDROID = auto()
    IOS = auto()

class BrowserName(Enum):
    CHROME = auto()
    FIREFOX = auto()
    SAFARI = auto()
    IE = auto()
    OPERA = auto()
    HTML = auto()

class AppiumAndroidBrowserName(Enum):
    BROWSER = auto()
    CHROME = auto()

class AppiumIosBrowserName(Enum):
    SAFARI = auto()

class FileFormat(Enum):
    INI = auto()
    TXT = auto()
    DELIMITED = auto()
    XLS = auto()
    CSV = auto()
    GNS = auto()

class DataFileFormat(Enum):
    INI = auto()
    TXT = auto()
    DELIMITED = auto()
    XLS = auto()
    CSV = auto()

class Order(Enum):
    RETAIN = auto()
    BY_NAME = auto()
    RANDOM = auto()

class Filter(Enum):
    INCLUDE = auto()
    EXCLUDE = auto()

class GuiAutomationContext(Enum):
    WEB = auto()
    NATIVE = auto()
    SCREEN = auto()
    ANDROID_WEB = auto()
    IOS_WEB = auto()
    ANDROID_NATIVE = auto()
    IOS_NATIVE = auto()

    # DESKTOP_CONTEXTS = {GuiAutomationContext.NATIVE, GuiAutomationContext.WEB}
    # MOBILE_WEB_CONTEXTS = {GuiAutomationContext.ANDROID_WEB, GuiAutomationContext.IOS_WEB}
    # ALL_WEB_CONTEXTS = {GuiAutomationContext.WEB, GuiAutomationContext.ANDROID_WEB, GuiAutomationContext.IOS_WEB}
    # MOBILE_NATIVE_CONTEXTS = {GuiAutomationContext.ANDROID_NATIVE, GuiAutomationContext.IOS_NATIVE}
    
    @staticmethod
    def isDesktopContext(context):
        return context in GuiAutomationContext.DESKTOP_CONTEXTS

    @staticmethod
    def is_mobile_web_context(context):
        return context in GuiAutomationContext.MOBILE_WEB_CONTEXTS

    @staticmethod
    def is_mobile_native_context(context):
        return context in GuiAutomationContext.MOBILE_NATIVE_CONTEXTS

    @staticmethod
    def is_web_context(context):
        return context in GuiAutomationContext.ALL_WEB_CONTEXTS

class GuiAutomatorName(Enum):
    SELENIUM = auto()
    APPIUM = auto()

class GuiElementType(Enum):
    TEXTBOX = auto()
    PASSWORD = auto()
    LINK = auto()
    BUTTON = auto()
    SUBMIT_BUTTON = auto()
    DROPDOWN = auto()
    CHECKBOX = auto()
    RADIO = auto()
    IMAGE = auto()

class OS(Enum):
	WINDOWS = auto()
	MAC = auto()
	LINUX = auto()
	ANDROID = auto()
	IOS = auto()

class MobileView(Enum):
    NATIVE_APP = auto()
    WEBVIEW = auto()

class Device(Enum):
    PC = auto()
    MOBILE = auto()
    GENERIC = auto()    

class Device(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()



class LoggingLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    FATAL = auto()

class ConfigPropertyFormattingTypeEnum(Enum):
    PATH_TO_ABS_PATH = auto()

class DeviceTypeEnum(Enum):
    PC = auto()
    MOBILE = auto()
    GENERIC = auto()

class HoconSyntaxTypeEnum(Enum):
    PROPERTIES = auto()
    JSON = auto()
    CONF = auto()


class FilterTypeEnum(Enum):
    INCLUDE = auto()
    EXCLUDE = auto()


class DiscoveredFileAttributeEnum(Enum):
    NAME = auto()
    EXTENSION = auto()
    FULL_NAME = auto()
    DIRECTORY_ABSOLUTE_PATH = auto()
    DIRECTORY_RELATIVE_PATH = auto()
    PACKAGE_DOT_NOTATION = auto()
    COMMA_SEPATARED_RELATIVE_PATH = auto()
    CONTAINER = auto()
    CONTAINER_TYPE = auto()

class ValueType(Enum):
    BOOLEAN = auto()
    STRING = auto()
    STRING_LIST = auto()
    NONE = auto()
    NUMBER = auto()
    NUMBER_LIST = auto()
    LIST = auto()
    ANYREF = auto()
    ENUM = auto()
    ENUM_LIST = auto()
    INTEGER = auto()
    OBJECT_LIST = auto()
    FLOAT = auto()
    DOUBLE = auto()
    LONG = auto()
    NOT_SET = auto()
    NA = auto()
    INT_LIST = auto()

class NamesContainerTypeEnum(Enum):
    TEST = auto()
    TEST_RESULT = auto()
    IGNORED_TEST = auto()
    STEP_RESULT = auto()
    ISSUE = auto()
    DEFAULT_FIXTURE_tfuncs = auto()
    COMPONENT_NAMES = auto()
    TEST_OBJECT = auto()
    EXCLUDED_TEST_RESULT = auto()
    EVENT = auto()
    TEST_OTYPE_NAMES = auto()
    FIXTURE_RESULT = auto()

class ConfigPropertyLevelEnum(Enum):
    CENTRAL = auto()
    THREAD = auto()

class CorePropertyTypeEnum(Enum):
    ARJUNA_ROOT_DIR = auto()
    PROG = auto()
    CONFIG_CENTRAL_FILE_NAME = auto()
    CONFIG_PROJECTS_DIR = auto()
    WORKSPACE_DIR = auto()
    EXTERNAL_TOOLS_DIR = auto()
    EXTERNAL_IMP_DIR = auto()
    LOGGER_DIR = auto()
    CONFIG_DIR = auto()
    LOGGER_CONSOLE_LEVEL = auto()
    LOGGER_FILE_LEVEL = auto()
    LOGGER_NAME = auto()
    PROJECT_DIRS_FILES = auto()

class GuiInteractionConfigType(Enum):
    CHECK_TYPE = auto()
    CHECK_PRE_STATE = auto()
    CHECK_POST_STATE = auto()
    SCROLL_TO_VIEW = auto()

class ReportFormat(Enum):
    XML = auto()
    HTML = auto()