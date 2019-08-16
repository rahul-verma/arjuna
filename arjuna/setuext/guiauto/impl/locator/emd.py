import re
from enum import Enum, auto
from collections import namedtuple

class MobileNativeLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    PARTIAL_LINK_TEXT = auto() 
    TAG_NAME = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class MobileWebLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    PARTIAL_LINK_TEXT = auto() 
    TAG_NAME = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class NativeLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    PARTIAL_LINK_TEXT = auto() 
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class VisualLocateWith(Enum):
    IMAGE = auto()

class WebLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    PARTIAL_LINK_TEXT = auto() 
    TAG_NAME = auto()
    CLASS_NAMES = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    ATTR_VALUE = auto()
    ATTR_PARTIAL_VALUE = auto()
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class GenericLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    PARTIAL_LINK_TEXT = auto() 
    TAG_NAME = auto()
    CLASS_NAMES = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    ATTR_VALUE = auto()
    ATTR_PARTIAL_VALUE = auto()
    IMAGE_SRC = auto()
    IMAGE = auto()
    INDEX = auto()

Locator = namedtuple("Locator", ("ltype", "lvalue"))
GuiGenericLocator = namedtuple("GuiGenericLocator", ("ltype", "lvalue"))

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

class GuiElementMetaData:
    XPATH_TWO_ARG_VALUE_PATTERN = r'^\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]$'

    BASIC_LOCATORS = {
        GenericLocateWith.ID,
        GenericLocateWith.NAME,
        GenericLocateWith.CLASS_NAME,
        GenericLocateWith.LINK_TEXT,
        GenericLocateWith.PARTIAL_LINK_TEXT,
        GenericLocateWith.XPATH,
        GenericLocateWith.CSS_SELECTOR,
        GenericLocateWith.TAG_NAME,
        GenericLocateWith.IMAGE,
        GenericLocateWith.INDEX,
    }

    XTYPE_LOCATORS = {
        GuiElementType.TEXTBOX: "//input[@type='text']",
        GuiElementType.PASSWORD: "//input[@type='password']",
        GuiElementType.LINK: "//a",
        GuiElementType.BUTTON: "//input[@type='button']",
        GuiElementType.SUBMIT_BUTTON: "//input[@type='submit']",
        GuiElementType.DROPDOWN: "//select",
        GuiElementType.CHECKBOX: "//input[@type='checkbox']",
        GuiElementType.RADIO: "//input[@type='radio']",
        GuiElementType.IMAGE: "//img",
    }

    XPATH_LOCATORS = {
        GenericLocateWith.TEXT : "//*[text()='{}']",
        GenericLocateWith.PARTIAL_TEXT : "//*[contains(text(),'{}')]",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    XPATH_TWO_ARG_LOCATORS = {
        GenericLocateWith.ATTR_VALUE : "//*[@{}='{}']",
        GenericLocateWith.ATTR_PARTIAL_VALUE : "//*[contains(@{},'{}')]"
    }

    def __init__(self, raw_locators):
        self.__raw_locators = raw_locators
        self.__locators = []
        self.__process()

    @property
    def locators(self):
        return self.__locators

    @property
    def raw_locators(self):
        return self.__raw_locators

    def __process(self):
        for raw_locator in self.__raw_locators:
            rltype = raw_locator.ltype
            rlvalue = raw_locator.lvalue
            try:
                generic_locate_with = GenericLocateWith[rltype.upper()]
            except:
                raise Exception("Invalid locator across all automators: {}".format(rltype))
            else:
                if generic_locate_with in self.BASIC_LOCATORS:
                    self.__add_locator(generic_locate_with, rlvalue)
                elif generic_locate_with in self.XPATH_LOCATORS:
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_LOCATORS[generic_locate_with].format(rlvalue))
                elif generic_locate_with in self.XPATH_TWO_ARG_LOCATORS:
                    parts = None
                    try:
                        parts =  re.search(GuiElementMetaData.XPATH_TWO_ARG_VALUE_PATTERN, rlvalue).groups()
                        print(parts)
                    except:
                        raise Exception("Value {} for {} is misformatted. Attribute name and attribute value should be supplied as: [<arg>][<value>]".format(rlvalue, rltype))
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_TWO_ARG_LOCATORS[generic_locate_with].format(parts[0], parts[1]))
                elif generic_locate_with == GenericLocateWith.TYPE:
                    try:
                        elem_type = GuiElementType[rlvalue.upper()]
                    except:
                        raise Exception("Unsupported element type for XTYPE locator: " + rlvalue)
                    else:
                        self.__add_locator(GenericLocateWith.XPATH, self.XTYPE_LOCATORS[elem_type])
                elif generic_locate_with == GenericLocateWith.CLASS_NAMES:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', "." + rlvalue.replace('.', ' ').strip()))
                else:
                    raise Exception("Locator not supported yet by Setu: " + rltype)

    def __add_locator(self, locator_type, locator_value):
        self.locators.append(GuiGenericLocator(locator_type, locator_value))

    @classmethod
    def createEMD(self, locators):
        processed_locators = []
        for locator in locators:
            processed_locators.append(
                Locator(ltype=locator["withType"], lvalue=locator["withValue"])
            )
        return GuiElementMetaData(processed_locators)

class SimpleGuiElementMetaData(GuiElementMetaData):

    def __init__(self, locator_type, locator_value):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value)])
