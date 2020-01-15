import re
from enum import Enum, auto
from collections import namedtuple

from arjuna.core.enums import GuiElementType

ImplWith = namedtuple('ImplWith' , ["wtype", "wvalue", "pos_args", "named_args", "has_content_locator"])

class MobileNativeLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
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
    LINK_PTEXT = auto() 
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
    LINK_PTEXT = auto() 
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
    LINK_PTEXT = auto() 
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
    LINK_PTEXT = auto() 
    TAG_NAME = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    PARTIAL_WINDOW_TITLE = auto()
    CONTENT_LOCATOR = auto()
    POINT = auto()
    JAVASCRIPT = auto()   

    #Translated to CSS Selectors
    COMPOUND_CLASS = auto()
    CLASS_NAMES = auto()

    # Translated to XPath
    TEXT = auto() 
    TITLE = auto() 
    PTEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    ATTR_VALUE = auto()
    ATTR_PVALUE = auto()
    IMAGE_SRC = auto()
    IMAGE = auto()

    # These need to be translated to
    PARTIAL_LINK_TEXT = auto()

class Locator:

    def __init__(self, ltype, lvalue, pos_args, named_args):
        self.ltype = ltype
        self.lvalue = lvalue
        self.__pos_args = pos_args
        self.__named_args = named_args

    def set_args(self,  pos_args, named_args):
        self.__pos_args = pos_args
        self.__named_args = named_args

    @property
    def pos_args(self):
        return self.__pos_args

    @property
    def named_args(self):
        return self.__named_args

    def __str__(self):
        return str(vars(self))

    def is_layered_locator(self):
        return False

class GuiGenericLocator(Locator):

    def __init__(self, ltype, lvalue, pos_args, named_args):
        super().__init__(ltype, lvalue, pos_args, named_args)
    
    def set_value(self, value):
        self.lvalue = value

class GuiGenericChildLocator(Locator):
    def __init__(self, ltype, lvalue, pos_args, named_args):
        super().__init__(ltype, lvalue, pos_args, named_args)
    
    def set_value(self, value):
        self.lvalue = value    

    def is_layered_locator(self):
        return True

class GuiElementMetaData:
    XPATH_TWO_ARG_VALUE_PATTERN = r'^\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]$'

    BASIC_LOCATORS = {
        GenericLocateWith.ID,
        GenericLocateWith.NAME,
        GenericLocateWith.CLASS_NAME,
        GenericLocateWith.LINK_TEXT,
        GenericLocateWith.XPATH,
        GenericLocateWith.CSS_SELECTOR,
        GenericLocateWith.TAG_NAME,
        GenericLocateWith.IMAGE,
        GenericLocateWith.INDEX,
        GenericLocateWith.WINDOW_TITLE,
        GenericLocateWith.PARTIAL_WINDOW_TITLE,
        GenericLocateWith.POINT,
        GenericLocateWith.JAVASCRIPT,
    }

    NEED_TRANSLATION = {
        GenericLocateWith.LINK_PTEXT : GenericLocateWith.PARTIAL_LINK_TEXT
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
        GenericLocateWith.PTEXT : "//*[contains(text(),'{}')]",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    XPATH_TWO_ARG_LOCATORS = {
        GenericLocateWith.ATTR_VALUE : "//*[@{}='{}']",
        GenericLocateWith.ATTR_PVALUE : "//*[contains(@{},'{}')]"
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
            pos_args = raw_locator.pos_args
            named_args = raw_locator.named_args
            try:
                generic_locate_with = GenericLocateWith[rltype.upper()]
            except:
                raise Exception("Invalid locator across all automators: {}".format(rltype))
            else:
                if generic_locate_with == GenericLocateWith.CONTENT_LOCATOR:
                    self.__add_locator(generic_locate_with, rlvalue, pos_args, named_args)
                elif generic_locate_with in self.BASIC_LOCATORS:
                    self.__add_locator(generic_locate_with, rlvalue, pos_args, named_args)
                elif generic_locate_with in self.NEED_TRANSLATION:
                    self.__add_locator(self.NEED_TRANSLATION[generic_locate_with], rlvalue, pos_args, named_args)
                elif generic_locate_with in self.XPATH_LOCATORS:
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_LOCATORS[generic_locate_with].format(rlvalue), pos_args, named_args)
                elif generic_locate_with in self.XPATH_TWO_ARG_LOCATORS:
                    parts = None
                    try:
                        parts =  re.search(GuiElementMetaData.XPATH_TWO_ARG_VALUE_PATTERN, rlvalue).groups()
                    except:
                        raise Exception("Value {} for {} is misformatted. Attribute name and attribute value should be supplied as: [<arg>][<value>]".format(rlvalue, rltype))
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_TWO_ARG_LOCATORS[generic_locate_with].format(parts[0], parts[1]), pos_args, named_args)
                elif generic_locate_with == GenericLocateWith.TYPE:
                    try:
                        elem_type = GuiElementType[rlvalue.upper()]
                    except:
                        raise Exception("Unsupported element type for XTYPE locator: " + rlvalue)
                    else:
                        self.__add_locator(GenericLocateWith.XPATH, self.XTYPE_LOCATORS[elem_type], pos_args, named_args)
                elif generic_locate_with == GenericLocateWith.COMPOUND_CLASS:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', "." + rlvalue.replace('.', ' ').strip()), pos_args, named_args)
                elif generic_locate_with == GenericLocateWith.CLASS_NAMES:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, "." + ".".join(rlvalue), pos_args, named_args)
                else:
                    raise Exception("Locator not supported yet by Setu: " + rltype)

    def __add_locator(self, locator_type, locator_value, pos_args, named_args):
        self.locators.append(GuiGenericLocator(locator_type, locator_value, pos_args, named_args))

    def process_args(self):
        '''
            It consumes impl locator list.
        '''
        pattern = r"$(\w*?)$"
        for locator in self.locators:
            if locator.ltype == GenericLocateWith.CONTENT_LOCATOR:
                locator.lvalue.process_args()

            if not locator.pos_args and not locator.named_args: continue

            fmt_locator_value = locator.lvalue.replace("\{", "LEFT_BRACE").replace("}", "RIGHT_BRACE")

            # Find params
            matches = re.findall(pattern, fmt_locator_value)
            matches = [match.lower() for match in matches]

            for match in matches:
                fmt_locator_value.replace(match, "\{{}\}".format(match.group(1)))

            fmt_locator_value.format(*locator.pos_args, **locator.named_args)

            locator.set_value(fmt_locator_value)


    @classmethod
    def __process_single_raw_locator(cls, impl_locator):
        ltype = impl_locator.wtype
        lvalue = impl_locator.wvalue
        p_locator = Locator(ltype=ltype, lvalue=lvalue, pos_args=impl_locator.pos_args, named_args=impl_locator.named_args)
        return p_locator

    @classmethod
    def convert_to_impl_with_locators(cls, *with_locators):
        return (l.as_impl_locator() for l in with_locators)

    @classmethod
    def create_emd(cls, *locators):
        impl_locators = cls.convert_to_impl_with_locators(*locators)
        processed_locators = []
        for locator in impl_locators:
            ltype = locator.wtype.lower()
            if ltype == "CONTENT_LOCATOR":
                CONTENT_LOCATOR = cls.create_emd(locator.wvalue)
                p_locator = Locator(ltype=locator.wtype, lvalue=CONTENT_LOCATOR)
            else:
                p_locator = cls.__process_single_raw_locator(locator)
            processed_locators.append(p_locator)
        return GuiElementMetaData(processed_locators)

class SimpleGuiElementMetaData(GuiElementMetaData):

    def __init__(self, locator_type, locator_value):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value)])
