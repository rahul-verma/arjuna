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

from enum import Enum, auto

class DataSourceTypeEnum(Enum):
    DATA = auto()
    DATA_ARRAY = auto()
    DATA_METHOD = auto()
    DATA_FILE = auto()
    DATA_GENERATOR = auto()

class UniteeComponentEnum(Enum):
    TEST_RUNNER = auto()
    TEST_FILTER = auto()

class IssueSubType(Enum):
    pass

class ResultCodeEnum(Enum):
    ERROR_INIT_MODULE = auto()
    ERROR_END_MODULE = auto()
    ERROR_INIT_EACH_FUNCTION = auto()
    ERROR_END_EACH_FUNCTION = auto()
    ERROR_INIT_EACH_TEST = auto()
    ERROR_END_EACH_TEST = auto()
    FAIL_INIT_MODULE = auto()
    FAIL_END_MODULE = auto()
    FAIL_INIT_EACH_FUNCTION = auto()
    FAIL_END_EACH_FUNCTION = auto()
    FAIL_INIT_EACH_TEST = auto()
    FAIL_END_EACH_TEST = auto()

    FAIL_CHILD_TEST_OBJECT = auto()
    ERROR_CHILD_TEST_OBJECT = auto()
    EXCLUDED_CHILD_TEST_OBJECT = auto()
    PASS_ALL_CHILD_TEST_OBJECTS = auto()

    PASS_ALL_STEPS = auto()

    DATASOURCE_CONSTRUCTION_ERROR = auto()
    DEPENDENCY_NOT_MET = auto()
    PARENT_DEPENDENCY_NOT_MET = auto()

    SURRENDERED_RULES_NOT_MET = auto()
    PARENT_SURRENDERED = auto()

    STEP_FAILURE = auto()
    STEP_ERROR = auto()
    SKIPPED_RECORD = auto()
    TEST_CONTAINER_DEPENDENCY_NOTMET = auto()
    tfunc_DEPENDENCY_NOTMET = auto()
    TEST_CONTAINER_CONSTRUCTOR_ERROR = auto()
    ERROR_IN_BEFORE_CLASS = auto()
    ERROR_IN_BEFORE_CLASS_INSTANCE = auto()
    ERROR_IN_BEFORE_CLASS_FRAGMENT = auto()
    ERROR_IN_BEFORE_METHOD = auto()
    ERROR_IN_BEFORE_METHOD_INSTANCE = auto()
    ERROR_IN_BEFORE_TEST = auto()
    ERROR_IN_AFTER_CLASS = auto()
    ERROR_IN_AFTER_CLASS_INSTANCE = auto()
    ERROR_IN_AFTER_CLASS_FRAGMENT = auto()
    ERROR_IN_AFTER_METHOD = auto()
    ERROR_IN_AFTER_METHOD_INSTANCE = auto()
    ERROR_IN_AFTER_TEST = auto()

    dsource_NEXT_ERROR = auto()

class IgnoredTestStatusEnum(Enum):
    UNPICKED = auto()
    SKIPPED = auto()

class IgnoredTestReasonEnum(Enum):
    UNPICKED_CLASS = auto()
    UNPICKED_METHOD = auto()
    SKIPPED_CLASS_ANNOTATION = auto()
    SKIPPED_METHOD_ANNOTATION = auto()

class DeferredReporterNames(Enum):
    EXCEL = auto()
    JXML = auto()

class UnpickedCodeEnum(Enum):
    UNPICKED_CLASS = auto()
    UNPICKED_METHOD = auto()

class ActiveReporterNames(Enum):
    MIN_CONSOLE = auto()
    CONSOLE = auto()
    EXCEL = auto()


class DataRecordOrderEnum(Enum):
    ORDERED = auto()
    UNORDERED = auto()


class SkipCodeEnum(Enum):
    SKIP_MODULE_DEC = auto()
    SKIP_FUNC_DEC = auto()
    SKIP_REC_DEC = auto()

class UserDefinedPropertyEnum(Enum):
    UNKNOWN = auto()

class UniteePropertyEnum(Enum):
    SESSION_NAME = auto()
    RUNID = auto()
    IRUNID = auto()
    FAILFAST = auto()
    PROJECT_NAME = auto()
    PROJECT_DIR = auto()
    PROJECT_CONFIG_DIR = auto()
    TEST_MODULE_IMPORT_PREFIX = auto()
    CONF_FIXTURES_IMPORT_PREFIX = auto()
    DATA_DIR = auto()
    DATA_SOURCES_DIR = auto()
    DATA_REFERENCES_DIR = auto()
    SCREENSHOTS_DIR = auto()
    SESSIONS_DIR = auto()
    GROUPS_DIR = auto()
    TESTS_DIR = auto()
    REPORT_DIR = auto()
    ARCHIVES_DIR = auto()
    CORE_DIR = auto()
    CORE_DB_CENTRAL_DIR = auto()
    CORE_DB_CENTRAL_DBFILE = auto()
    CORE_DB_RUN_DIR = auto()
    CORE_DB_RUN_DBFILE = auto()
    CORE_DB_TEMPLATE_DIR = auto()
    CORE_DB_TEMPLATE_CENTRAL_DBFILE = auto()
    CORE_DB_TEMPLATE_RUN_DBFILE = auto()
    RUN_REPORT_DIR = auto()
    RUN_REPORT_JDB_DIR = auto()
    RUN_REPORT_JSON_DIR = auto()
    RUN_REPORT_JSON_TESTS_DIR = auto()
    RUN_REPORT_JSON_ISSUES_DIR = auto()
    RUN_REPORT_JSON_IGNOREDTESTS_DIR = auto()
    RUN_REPORT_JSON_EVENTS_DIR = auto()
    RUN_REPORT_JSON_FIXTURES_DIR = auto()
    REPORT_NAME_FORMAT = auto()
    ACTIVE_REPORTERS = auto()
    DEFERRED_REPORTERS = auto()
    OFFLINE_REPORTERS = auto()

class DependencyConditionEnum(Enum):
    NO_ISSUES = auto()
    NONE = auto()

class IssueTypeEnum(Enum):
    FIXTURE_STEP_ISSUE = auto()
    DATA_SOURCE_ISSUE = auto()
    TEST_STEP_ISSUE = auto()

class FixtureTypeEnum(Enum):
    INIT_SESSION = auto()
    END_SESSION = auto()
    INIT_EACH_STAGE = auto()
    END_EACH_STAGE = auto()
    INIT_STAGE = auto()
    END_STAGE = auto()
    INIT_EACH_GROUP = auto()
    END_EACH_GROUP = auto()
    INIT_GROUP = auto()
    END_GROUP = auto()
    INIT_EACH_MODULE = auto()
    END_EACH_MODULE = auto()
    INIT_MODULE = auto()
    INIT_EACH_FUNCTION = auto()
    INIT_EACH_TEST = auto()
    END_EACH_TEST = auto()
    END_EACH_FUNCTION = auto()
    END_MODULE = auto()

class IssueSubTypeEnum(Enum):
    FIXTURE_BEFORE_SESSION = auto()
    FIXTURE_AFTER_SESSION = auto()
    FIXTURE_BEFORE_GROUP = auto()
    FIXTURE_AFTER_GROUP = auto()
    FIXTURE_BEFORE_CLASS = auto()
    FIXTURE_AFTER_CLASS = auto()
    FIXTURE_BEFORE_CLASS_INSTANCE = auto()
    FIXTURE_AFTER_CLASS_INSTANCE = auto()
    FIXTURE_BEFORE_CLASS_FRAGMENT = auto()
    FIXTURE_AFTER_CLASS_FRAGMENT = auto()
    FIXTURE_BEFORE_METHOD = auto()
    FIXTURE_AFTER_METHOD = auto()
    FIXTURE_BEFORE_METHOD_INSTANCE = auto()
    FIXTURE_AFTER_METHOD_INSTANCE = auto()
    FIXTURE_BEFORE_TEST = auto()
    FIXTURE_AFTER_TEST = auto()
    CONSTRUCTOR = auto()
    STEP_FAILURE = auto()
    STEP_ERROR = auto()
    dsource_CONSTRUCTION = auto()
    dsource_NEXT_EXCEPTION = auto()

class PickerRuleEnum(Enum):
    CM = auto()
    IM = auto()
    CF = auto()
    IF = auto()

class ResultTypeEnum(Enum):
    PASS = auto()
    FAIL = auto()
    ERROR = auto()
    EXCLUDED = auto()
    EXCLUDED_CHILDREN = auto()
    UNPICKED = auto()
    SKIPPED = auto()
    NOT_A_TEST = auto()
    NOTHING = auto()
    SURRENDERED = auto()

class ReportableType(Enum):
    INFO = auto()
    RESULT = auto()
    ISSUE = auto()

class TestObjectTypeEnum(Enum):
    Session = auto()
    Stage = auto()
    Group = auto()
    GSlot = auto()
    Module = auto()
    MSlot = auto()
    Function = auto()
    Test = auto()
    Fixture = auto()
    Step = auto()

class InfoType(Enum):
    STARTED = auto()
    FINISHED = auto()

class InfoEntryEnum(Enum):
    INFO_TIMESTAMP = auto()
    OTYPE = auto()
    MESSAGE = auto()
    SESSION = auto()
    STAGE = auto()
    GROUP = auto()
    PKG = auto()
    MODULE = auto()
    FUNCTION = auto()
    TEST = auto()
    FIXTURE = auto()
    FIXTYPE = auto()
    BTSTAMP = auto()
    ETSTAMP = auto()
    EXEC_TIME = auto()

class ResultEntryEnum(Enum):
    RESULT_TIMESTAMP = auto()
    OTYPE = auto()
    SESSION = auto()
    STAGE = auto()
    GROUP = auto()
    PKG = auto()
    MODULE = auto()
    FUNCTION = auto()
    TEST = auto()
    FIXTURE = auto()
    FIXTYPE = auto()
    RTYPE = auto()
    RCODE = auto()
    PROPS = auto()
    RUNTIME = auto()
    EVARS = auto()
    TAGS = auto()
    DATA_RECORD = auto()
    IID = auto()
    THREAD_ID = auto()

class ExecutionContext(Enum):
    Fixture = auto()
    Test = auto()

class StepType(Enum):
    ExecStep = auto()
    AssertStep = auto()
    LogStep = auto()

class StepEntryEnum(Enum):
    OTYPE = auto()
    STEP_TIMESTAMP = auto()
    STEP_ID = auto()
    STEP_EXEC_CONTEXT = auto()
    STEP_TYPE = auto()
    STEP_SOURCE = auto()
    PURPOSE = auto()
    STEP_RTYPE = auto()
    IID = auto()
    OBSERVATION = auto()
    EXPECTATION = auto()
    ASSERT_MESSAGE = auto()
    STEP_PROPS = auto()

class IssueEntryEnum(Enum):
    ISSUE_TIMESTAMP = auto()
    IID = auto()
    ITYPE = auto()
    ISTYPE = auto()
    ENAME = auto()
    EMESSAGE = auto()
    ETRACE = auto()
    RESULT_TIMESTAMP = auto()
    OTYPE = auto()
    MESSAGE = auto()
    SESSION = auto()
    STAGE = auto()
    GROUP = auto()
    PKG = auto()
    MODULE = auto()
    FUNCTION = auto()
    TEST = auto()
    FIXTURE = auto()
    FIXTYPE = auto()
    RTYPE = auto()
    RCODE = auto()
    PROPS = auto()
    RUNTIME = auto()
    EVARS = auto()
    TAGS = auto()
    DATA_RECORD = auto()
    STEP_TIMESTAMP = auto()
    STEP_ID = auto()
    STEP_EXEC_CONTEXT = auto()
    STEP_TYPE = auto()
    STEP_SOURCE = auto()
    PURPOSE = auto()
    STEP_RTYPE = auto()
    OBSERVATION = auto()
    EXPECTATION = auto()
    ASSERT_MESSAGE = auto()
    STEP_PROPS = auto()
    THREAD_ID = auto()

class BuiltInProp(Enum):
    ID = auto()
    PRIORITY = auto()
    THREADS= auto()
    NAME = auto()
    AUTHOR = auto()
    IDEA = auto()
    UNSTABLE = auto()
    COMPONENT = auto()
    APP_VERSION = auto()