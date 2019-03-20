'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

import enum

from enum import Enum, auto

class FileFormatEnum(Enum):
    INI = auto()
    TXT = auto()
    DELIMITED = auto()
    XLS = auto()
    CSV = auto()

class LoggingLevelEnum(Enum):
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

class BrowserEnum(Enum):
    CHROME = auto()
    FIREFOX = auto()
    SAFARI = auto()
    IE = auto()
    OPERA = auto()
    HTML = auto()

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

class ValueTypeEnum(Enum):
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