from enum import Enum, auto

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

class GuiActionConfigType(Enum):
    CHECK_TYPE = auto()
    CHECK_PRE_STATE = auto()
    CHECK_POST_STATE = auto()