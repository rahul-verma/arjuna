from enum import Enum, auto

class ArjunaOption(Enum):
    ROOT_DIR = auto()
    LOG_DIR = auto()
    DATA_DIR = auto()
    DATA_SOURCES_DIR = auto()
    DATA_REFERENCES_DIR = auto()
    SCREENSHOTS_DIR = auto()
    GUIAUTO_NAMESPACE_DIR = auto()
    PROJECT_CONF_DIR = auto()
    PROJECT_CONF_FILE = auto()

    SETUACTOR_GUIAUTO_MODE = auto()
    SETUACTOR_GUIAUTO_URL = auto()

    APP_URL = auto()

    TESTRUN_ENVIRONMENT = auto()

    GUIAUTO_AUTOMATOR_NAME = auto()

    BROWSER_NAME = auto()
    BROWSER_VERSION = auto()
    BROWSER_MAXIMIZE = auto()
    BROWSER_DIM_HEIGHT = auto()
    BROWSER_DIM_WIDTH = auto()
    BROWSER_BIN_PATH = auto()
    BROWSER_PROXY_ON = auto()

    GUIAUTO_CONTEXT = auto()
    GUIAUTO_SCROLL_PIXELS = auto()
    GUIAUTO_SWIPE_TOP = auto()
    GUIAUTO_SWIPE_BOTTOM = auto()
    GUIAUTO_SWIPE_MAX_WAIT = auto()
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