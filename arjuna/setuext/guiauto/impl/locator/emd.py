import re
from enum import Enum, auto
from collections import namedtuple
from arjuna.tpi.enums import ArgsType

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
    WINDOW_TITLE = auto()
    PARTIAL_WINDOW_TITLE = auto()

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
    WINDOW_TITLE = auto()
    PARTIAL_WINDOW_TITLE = auto()
    CHILD_LOCATOR = auto()

class Locator:

    def __init__(self, ltype, lvalue, args_type=None, args=None):
        self.ltype = ltype
        self.lvalue = lvalue
        self.__set_args_type(args_type)
        self.args = args

    def __set_args_type(self, args_type):
        if not args_type:
            self.args_type = None
        elif type(args_type) is str:
            self.args_type = ArgsType[args_type.upper()]
        else:
            self.args_type = args_type

    def set_args(self, args_type, args):
        self.__set_args_type(args_type)
        self.args = args

    def __str__(self):
        return str(vars(self))

    def is_layered_locator(self):
        return False

class GuiGenericLocator(Locator):

    def __init__(self, ltype, lvalue, args_type=None, args=None):
        super().__init__(ltype, lvalue, args_type, args)
    
    def set_value(self, value):
        self.lvalue = value

class GuiGenericChildLocator(Locator):
    def __init__(self, ltype, lvalue, args_type=None, args=None):
        super().__init__(ltype, lvalue, args_type, args)
    
    def set_value(self, value):
        self.lvalue = value    

    def is_layered_locator(self):
        return True

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
        GenericLocateWith.WINDOW_TITLE,
        GenericLocateWith.PARTIAL_WINDOW_TITLE
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

    def __init__(self, raw_locators, process_args=True):
        self.__raw_locators = raw_locators
        self.__locators = []
        self.__process()
        if process_args:
            self.process_args()

    def __str__(self):
        return str([str(l) for l in self.__locators])

    def print_locators(self):
        print(str(self))

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
            args_type = raw_locator.args_type
            args = raw_locator.args
            try:
                generic_locate_with = GenericLocateWith[rltype.upper()]
            except:
                raise Exception("Invalid locator across all automators: {}".format(rltype))
            else:
                if generic_locate_with == GenericLocateWith.CHILD_LOCATOR:
                    self.__add_locator(generic_locate_with, rlvalue, args_type, args)
                elif generic_locate_with in self.BASIC_LOCATORS:
                    self.__add_locator(generic_locate_with, rlvalue, args_type, args)
                elif generic_locate_with in self.XPATH_LOCATORS:
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_LOCATORS[generic_locate_with].format(rlvalue), args_type, args)
                elif generic_locate_with in self.XPATH_TWO_ARG_LOCATORS:
                    parts = None
                    try:
                        parts =  re.search(GuiElementMetaData.XPATH_TWO_ARG_VALUE_PATTERN, rlvalue).groups()
                    except:
                        raise Exception("Value {} for {} is misformatted. Attribute name and attribute value should be supplied as: [<arg>][<value>]".format(rlvalue, rltype))
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_TWO_ARG_LOCATORS[generic_locate_with].format(parts[0], parts[1]), args_type, args)
                elif generic_locate_with == GenericLocateWith.TYPE:
                    try:
                        elem_type = GuiElementType[rlvalue.upper()]
                    except:
                        raise Exception("Unsupported element type for XTYPE locator: " + rlvalue)
                    else:
                        self.__add_locator(GenericLocateWith.XPATH, self.XTYPE_LOCATORS[elem_type], args_type, args)
                elif generic_locate_with == GenericLocateWith.CLASS_NAMES:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', "." + rlvalue.replace('.', ' ').strip()), args_type, args)
                else:
                    raise Exception("Locator not supported yet by Setu: " + rltype)

    def __add_locator(self, locator_type, locator_value, args_type, args):
        self.locators.append(GuiGenericLocator(locator_type, locator_value, args_type, args))

    def process_args(self):
        pattern = r"(%\w+%)"
        for locator in self.locators:
            if locator.ltype == GenericLocateWith.CHILD_LOCATOR:
                locator.lvalue.process_args()

            if not locator.args_type: continue

            fmt_locator_value = locator.lvalue
            # Find params
            matches = re.findall(pattern, fmt_locator_value)
            matches = [match.lower() for match in matches]

            if locator.args_type == ArgsType.POSITIONAL:
                for index, match in enumerate(matches):
                    fmt_locator_value = fmt_locator_value.replace(match, "%{}%".format(index + 1))
                
            for arg in locator.args:
                target = "%{}%".format(arg["name"].lower())
                fmt_locator_value = fmt_locator_value.replace(target, arg["value"])

            locator.set_value(fmt_locator_value)


    @classmethod
    def __process_single_raw_locator(cls, locator):
        p_locator = None
        ltype = locator["withType"]
        lvalue = locator["withValue"]
        args_type = None
        args = None
        if "argsType" in locator:
            args_type = ArgsType[locator["argsType"]]
            args = locator["args"]
        p_locator = Locator(ltype=ltype, lvalue=lvalue, args_type=args_type, args=args)
        return p_locator

    @classmethod
    def createEMD(cls, locators):
        processed_locators = []
        for locator in locators:
            ltype = locator["withType"].lower()
            if ltype == "child_locator":
                child_locator = cls.createEMD([locator["withValue"]])
                p_locator = Locator(ltype=locator["withType"], lvalue=child_locator)
            else:
                p_locator = cls.__process_single_raw_locator(locator)
            processed_locators.append(p_locator)
        return GuiElementMetaData(processed_locators)

class SimpleGuiElementMetaData(GuiElementMetaData):

    def __init__(self, locator_type, locator_value):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value)])
