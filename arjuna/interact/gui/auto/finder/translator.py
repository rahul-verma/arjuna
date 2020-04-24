import re
from arjuna.core.constant import GuiElementType

from ._with import GuiGenericLocator
from .enums import GenericLocateWith

class LocatorTranslator:
    '''
        Translates With Constructs to what underlying engines understand.
    '''

    BASIC_LOCATORS = {
        GenericLocateWith.ID,
        GenericLocateWith.NAME,
        GenericLocateWith.XPATH,
        GenericLocateWith.IMAGE,
        GenericLocateWith.INDEX,
        GenericLocateWith.WINDOW_TITLE,
        GenericLocateWith.WINDOW_PTITLE,
        GenericLocateWith.JS,
    }

    NEED_TRANSLATION = {
        GenericLocateWith.TAG : GenericLocateWith.TAG_NAME,
        GenericLocateWith.LINK : GenericLocateWith.PARTIAL_LINK_TEXT,
        GenericLocateWith.FLINK : GenericLocateWith.LINK_TEXT,
        GenericLocateWith.SELECTOR : GenericLocateWith.CSS_SELECTOR,
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
        GenericLocateWith.TEXT : "//*[contains(text(),'{}')]",
        GenericLocateWith.FTEXT : "//*[text()='{}']",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    NAMED_ARG_LOCATORS = {
        GenericLocateWith.ATTR : "//*[contains(@{name},'{value}')]",
        GenericLocateWith.FATTR : "//*[@{name}='{value}']",
        GenericLocateWith.POINT : "return document.elementFromPoint({x}, {y})",
    }

    @classmethod
    def translate(cls, locator):
        rltype = locator.ltype
        rlvalue = locator.lvalue
        glvalue = None
        try:
            gltype = GenericLocateWith[rltype.upper()]
        except Exception as e:
            raise Exception("Invalid locator across all automators: {}={}. Error: {}".format(rltype, type(rlvalue), str(e)))
        else:
            if gltype == GenericLocateWith.ELEMENT:
                glvalue = rlvalue
            elif gltype in cls.BASIC_LOCATORS:
                glvalue = rlvalue
            elif gltype in cls.NEED_TRANSLATION:
                glvalue = rlvalue
                gltype = cls.NEED_TRANSLATION[gltype]
            elif gltype in cls.XPATH_LOCATORS:
                glvalue = cls.XPATH_LOCATORS[gltype].format(rlvalue)
                gltype = GenericLocateWith.XPATH
            elif gltype == GenericLocateWith.POINT:
                glvalue = cls.NAMED_ARG_LOCATORS[gltype].format(**rlvalue)
            elif gltype in cls.NAMED_ARG_LOCATORS:
                glvalue = cls.NAMED_ARG_LOCATORS[gltype].format(**rlvalue)
                gltype = GenericLocateWith.XPATH
            elif gltype == GenericLocateWith.CLASSES:
                css_string = None
                if type(rlvalue) is str:
                    css_string = "." + rlvalue.replace('.', ' ').strip()
                else:
                    if type(rlvalue[0]) is str:
                        css_string = "." + rlvalue[0].replace('.', ' ').strip()
                    else:
                        css_string = "." + ".".join(rlvalue[0])
                glvalue = re.sub(r'\s+', '.', css_string)
                gltype = GenericLocateWith.CSS_SELECTOR
            else:
                raise Exception("Locator not supported yet by Arjuna: " + rltype)
    
        return GuiGenericLocator(gltype, glvalue)