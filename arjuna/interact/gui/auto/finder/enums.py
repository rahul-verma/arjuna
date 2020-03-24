from enum import Enum, auto

class WithType(Enum):
    ID = auto()
    NAME = auto()
    CLASSES = auto()
    LINK = auto()
    FLINK = auto()
    TAG = auto()
    XPATH = auto()
    SELECTOR = auto()

    TEXT = auto()
    FTEXT = auto()
    BTEXT = auto()
    ETEXT = auto()
    TITLE = auto()
    ATTR = auto()
    FATTR = auto()
    BATTR = auto()
    EATTR = auto()
    ATTR_WORD = auto()
    TYPE = auto()
    VALUE = auto()
    POINT = auto()
    JS = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    WINDOW_PTITLE = auto()
    ELEMENT = auto()
    LABEL = auto()


class GenericLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    SELECTOR = auto()
    CLASSES = auto() 
    LINK = auto() 
    FLINK = auto()
    PLINK = auto() 
    TAG = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    WINDOW_PTITLE = auto()
    ELEMENT = auto()
    POINT = auto()
    JS = auto() 

    # Translated to XPath
    TEXT = auto() 
    FTEXT = auto() 
    TITLE = auto() 
    TYPE = auto() 
    VALUE = auto() 
    ATTR = auto()
    FATTR = auto()
    IMAGE_SRC = auto()
    IMAGE = auto()

    # Translated 1-1 to Selenium
    PARTIAL_LINK_TEXT = auto()
    LINK_TEXT = auto()
    TAG_NAME = auto()
    CSS_SELECTOR = auto()