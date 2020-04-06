from enum import Enum, auto

class ArjunaOption(Enum):
    ARJUNA_ROOT_DIR = auto()
    ARJUNA_EXTERNAL_TOOLS_DIR = auto()
    ARJUNA_EXTERNAL_IMPORTS_DIR = auto()
    LOG_NAME = auto()

    RUN_ID = auto()
    RUN_ENV_NAME = auto()
    RUN_ENV_CONF_DIR = auto()
    RUN_HOST_OS = auto()

    LOG_FILE_LEVEL = auto()
    LOG_CONSOLE_LEVEL = auto()
    LOG_ALLOWED_CONTEXTS = auto()

    L10N_LOCALE = auto()
    L10N_STRICT = auto()
    L10N_DIR = auto()
    L10N_EXCEL_DIR = auto()
    L10N_JSON_DIR = auto()

    PROJECT_NAME = auto()
    PROJECT_ROOT_DIR = auto()
    PROJECT_CONF_FILE = auto()

    TESTS_DIR = auto()
    REPORTS_DIR = auto()
    REPORT_FORMATS = auto()
    REPORT_DIR = auto()
    REPORT_XML_DIR = auto()
    REPORT_HTML_DIR = auto()
    LOG_DIR = auto()
    SCREENSHOTS_DIR = auto()
    CONF_DIR = auto()

    DATA_DIR = auto()
    DATA_SRC_DIR = auto()
    DATA_REF_DIR = auto()
    DATA_REF_COLUMN_DIR = auto()
    DATA_REF_ROW_DIR = auto()

    SETU_PROJECT_DIRS_FILES = auto()

    APP_URL = auto()

    SETU_GUIAUTO_ACTOR_MODE = auto()
    SETU_GUIAUTO_ACTOR_URL = auto()

    BROWSER_NAME = auto()
    BROWSER_HEADLESS = auto()
    BROWSER_VERSION = auto()
    BROWSER_MAXIMIZE = auto()
    BROWSER_DIM_HEIGHT = auto()
    BROWSER_DIM_WIDTH = auto()
    BROWSER_BIN_PATH = auto()
    BROWSER_PROXY_ON = auto()

    GUIAUTO_NAME = auto()
    GUIAUTO_DIR = auto()
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
    GUIAUTO_WITHX_YAML = auto()

    MOBILE_OS_NAME = auto()
    MOBILE_OS_VERSION = auto()
    MOBILE_DEVICE_NAME = auto()
    MOBILE_DEVICE_UDID = auto()
    MOBILE_APP_FILE_PATH = auto()

    SELENIUM_DRIVER_PROP = auto()
    SELENIUM_DRIVERS_DIR = auto()
    SELENIUM_DRIVER_PATH = auto()
    SELENIUM_DRIVER_DOWNLOAD = auto()
    SELENIUM_SERVICE_URL = auto()

    APPIUM_SERVICE_URL = auto()
    APPIUM_AUTO_LAUNCH = auto()

    IMG_COMP_MIN_SCORE = auto()

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
    LINUX = auto()

class SetuActorMode(Enum):
    LOCAL = auto()
    REMOTE = auto()

class MobileOsName(Enum):
    ANDROID = auto()
    IOS = auto()

class BrowserName(Enum):
    CHROME = auto()
    FIREFOX = auto()

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
    TRACE = auto()
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

class DataRefContextType(Enum):
    ROW = auto()
    COLUMN = auto()

class GuiTemplate(Enum):
    ELEMENT = auto()
    MULTI_ELEMENT = auto()
    DROPDOWN = auto()
    RADIO_GROUP = auto()

import locale
import re
__locales = [i.upper() for i in locale.locale_alias.keys() if re.match('^[\w_]+$', i)]
Locale = Enum('Locale', dict(zip(__locales, range(len(__locales)))))