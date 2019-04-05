from enum import Enum, auto


class ArjunaOption(Enum):
    ARJUNA_ROOT_DIR = auto()
    ARJUNA_EXTERNAL_TOOLS_DIR = auto()
    ARJUNA_EXTERNAL_IMPORTS_DIR = auto()
    PYTHON_LOG_NAME = auto()
    LOG_NAME = auto()

    LOG_DIR = auto()

    LOG_CONSOLE_LEVEL = auto()
    LOG_FILE_LEVEL = auto()

    PROJECT_NAME = auto()
    PROJECT_ROOT_DIR = auto()
    PROJECT_CONF_FILE = auto()

    DATA_DIR = auto()
    DATA_SOURCES_DIR = auto()
    DATA_REFERENCES_DIR = auto()
    SCREENSHOTS_DIR = auto()
    CONFIG_DIR = auto()

    SETU_PROJECT_DIRS_FILES = auto()
    REPORT_DIR = auto()
    ARCHIVES_DIR = auto()

    AUT_URL = auto()

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

class SetuActorMode(Enum):
    LOCAL = auto()
    REMOTE = auto()

class GuiAutomatorName(Enum):
    SELENIUM = auto()

class GuiAutomationContext(Enum):
	WEB = auto()
	NATIVE = auto()
	SCREEN = auto()
	ANDROID_WEB = auto()
	IOS_WEB = auto()
	ANDROID_NATIVE = auto()
	IOS_NATIVE = auto()

class BrowserName(Enum):
    FIREFOX = auto()
    SAFARI = auto()
    CHROME = auto()

class MobileOsName(Enum):
    ANDROID = auto()
    IOS = auto()

class DesktopOS(Enum):
    WINDOWS = auto()
    MAC = auto()
    LINUX = auto()