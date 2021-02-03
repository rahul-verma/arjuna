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

from enum import Enum, auto

class ModifierKey(Enum):
    CTRL = auto()
    CMD = auto()
    XCTRL = auto()
    ALT = auto()
    SHIFT = auto()

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

class DataRefType(Enum):
    CONTEXTUAL = auto()
    INDEXED = auto()

class LoggingLevel(Enum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    FATAL = auto()

class GuiWidgetType(Enum):
    ELEMENT = auto()
    MULTI_ELEMENT = auto()
    DROPDOWN = auto()
    RADIO_GROUP = auto()

class DryRunType(Enum):
    SHOW_TESTS = auto()
    SHOW_PLAN = auto()
    CREATE_RES = auto()

class BuiltInProp(Enum):
    PACKAGE = auto()
    MODULE = auto()
    QUAL_NAME = auto()
    ID = auto()
    PRIORITY = auto()
    THREADS= auto()
    NAME = auto()
    AUTHOR = auto()
    IDEA = auto()
    UNSTABLE = auto()
    COMPONENT = auto()
    APP_VERSION = auto()
    LEVEL = auto()
    REVIEWED = auto()

class RuleNature(Enum):
    INCLUDE = auto()
    EXCLUDE = auto()

class RuleType(Enum):
    SET = auto()
    DICT_KEY = auto()
    DICT_VALUE = auto()

class RuleTargetType(Enum):
    PROPS = auto()
    TAGS = auto()
    BUGS = auto()

class RuleConditionType(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()
    MATCHES = auto()
    DOES_NOT_MATCH = auto()
    PARTIALLY_MATCHES = auto()
    DOES_NOT_PARTIALLY_MATCH = auto()
    LESS_THAN = auto()
    LESS_OR_EQUAL = auto()
    GREATER_THAN = auto()
    GREATER_OR_EQUAL = auto()
    CONTAINS = auto()
    IS_SUBSET = auto()
    HAS_INTERSECTION = auto()
    NO_INTERSECTION = auto()

class ConfigStage(Enum):
    DEFAULT = auto()
    REFERENCE = auto()
    PROJECT = auto()
    CODED = auto()
    CLI = auto()