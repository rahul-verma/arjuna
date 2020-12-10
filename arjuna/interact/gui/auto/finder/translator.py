import re
from arjuna.core.constant import GuiElementType
from arjuna.tpi.constant import DomNodeType, DomDirection

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
        GenericLocateWith.BTEXT : "//*[starts-with(text(),'{}')]",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    NAMED_ARG_LOCATORS = {
        # GenericLocateWith.ATTR : "//*[contains(@{name},'{value}')]",
        # GenericLocateWith.FATTR : "//*[@{name}='{value}']",
        # GenericLocateWith.BATTR : "//*[starts-with(@{name},'{value}')]",
        # GenericLocateWith.EATTR : "//*[ends-with(@{name},'{value}')]",
        GenericLocateWith.ATTR : "*[{name}*='{value}']",
        GenericLocateWith.FATTR : "*[{name}='{value}']",
        GenericLocateWith.BATTR : "*[{name}^='{value}']",
        GenericLocateWith.EATTR : "*[{name}$='{value}']",
        GenericLocateWith.POINT : "return document.elementFromPoint({x}, {y})",
    }

    TEXT_TRANSLATIONS = {
        'text' : "text()",
        '*text' : "*//text()",
        'star_text' : "*//text()",
        '.text' : ".",
        'dot_text' : ".",
    }

    @classmethod
    def __process_selector(cls, cssvalue):
        css_string = None
        if type(cssvalue) is str:
            css_string = "." + cssvalue.replace('.', ' ').strip()
        else:
            if type(cssvalue[0]) is str:
                # Tuple like ('button button-large',)
                cssvalue = " ".join(cssvalue)
                css_string = "." + cssvalue.replace('.', ' ').strip()
            else:
                # Tuple is (('button', 'button-large'),)
                css_string = "." + ".".join(cssvalue[0])
        return re.sub(r'\s+', '.', css_string)

    @classmethod
    def __convert_to_class_list(cls, cssvalue):
        return cls.__process_selector(cssvalue)[1:].split(".")

    @classmethod
    def __process_tags(cls, tagsvalue):
        tag_list = None
        if type(tagsvalue) is str:
            tag_list = tagsvalue.strip().split()
        else:
            tag_list = tagsvalue
        return [t.lower()=='any' and '*' or t for t in tag_list]

    @classmethod
    def translate(cls, locator):
        from arjuna import log_debug
        rltype = locator.ltype
        rlvalue = locator.lvalue
        glvalue = None
        try:
            gltype = GenericLocateWith[rltype.upper()]
        except Exception as e:
            raise Exception("Invalid locator across all automators: {}={}. Error: {}".format(rltype, type(rlvalue), str(e)))
        else:
            log_debug("Processing locator: Type: {}; Value: {}".format(str(gltype), rlvalue))
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
                gltype = GenericLocateWith.CSS_SELECTOR
            elif gltype == GenericLocateWith.CLASSES:
                css_string = cls.__process_selector(rlvalue)
                glvalue = cls.__process_selector(rlvalue)
                gltype = GenericLocateWith.CSS_SELECTOR
            elif gltype == GenericLocateWith.TAGS:
                glvalue = " ".join(cls.__process_tags(rlvalue))
                gltype = GenericLocateWith.CSS_SELECTOR                
            elif gltype in {GenericLocateWith.NODE, GenericLocateWith.BNODE, GenericLocateWith.FNODE}:
                gltype, glvalue = cls.__translate_node(gltype, rlvalue)
            elif gltype == GenericLocateWith.AXES:
                gltype, glvalue = cls.__translate_axes(gltype, rlvalue)
            else:
                raise Exception("Locator not supported yet by Arjuna: " + rltype)    
        return GuiGenericLocator(gltype, glvalue)


    @classmethod
    def __translate_node_rlvalue_to_xpath(cls, gltype, rlvalue, prefix_slashes=True):
        xblocks = []
        tags = '*'
        for k,v in rlvalue.items():
            if k.lower() == 'tags':
                tags = "//".join(v)
                continue

            if k == "classes":
                for c in v:
                    xblocks.append(f"contains(@class,'{c}')")
                continue

            if k.lower() in cls.TEXT_TRANSLATIONS:
                k = cls.TEXT_TRANSLATIONS[k.lower()]
            else:
                k = f'@{k}'
            if gltype == GenericLocateWith.NODE:
                xblocks.append(f"contains({k},'{v}')")
            elif gltype == GenericLocateWith.BNODE:
                xblocks.append(f"starts-with({k},'{v}')")
            elif gltype == GenericLocateWith.FNODE:
                xblocks.append(f"{k}='{v}'")
        if xblocks:
            xblocks_str = "[" + " and ".join(xblocks) + "]"
        else:
            xblocks_str = ""
        
        if prefix_slashes:
            prefix = "//"
        else:
            prefix = ""
        glvalue = f"{prefix}{tags}{xblocks_str}"
        gltype = GenericLocateWith.XPATH
        return gltype, glvalue

    @classmethod
    def __translate_node_to_selector(cls, gltype, rlvalue):
        cblocks = []
        tags = '*'
        classes = ""
        for k,v in rlvalue.items():
            if k.lower() == 'tags':
                tags = " ".join(v)
                continue

            if k == "classes":
                classes = "." + ".".join(v)
                continue
            
            if gltype == GenericLocateWith.NODE:
                cblocks.append(f"[{k}*='{v}']")
            elif gltype == GenericLocateWith.BNODE:
                cblocks.append(f"[{k}^='{v}']")
            elif gltype == GenericLocateWith.FNODE:
                cblocks.append(f"[{k}='{v}']")
        if cblocks:
            cblocks_str = "".join(cblocks)
        else:
            cblocks_str = ""
        glvalue = f"{tags}{classes}{cblocks_str}"
        gltype = GenericLocateWith.CSS_SELECTOR
        return gltype, glvalue


    @classmethod
    def __process_node_rlvalue_and_xpath_condition(cls, rlvalue):
        lkeys = [k.lower() for k in rlvalue.keys()]
        if 'tag' in lkeys and 'tags' in lkeys:
            raise Exception("node Locator definition can contain either 'tag' or 'tags' as key.")
        if len(set(lkeys).intersection(set(cls.TEXT_TRANSLATIONS.keys()))) > 1:
            raise Exception("node Locator definition can contain only one of text/star_text/*text/dot_text/.text keys.")
        # Initial processing
        updated_rlvalue = dict()
        use_xpath = False
        for k,v in rlvalue.items():
            if k.lower() == 'tag':
                updated_rlvalue['tags'] = cls.__process_tags(v)
            elif k.lower() == 'tags':
                updated_rlvalue['tags'] = cls.__process_tags(v)
            elif k.lower() == 'classes':
                updated_rlvalue['classes'] = cls.__convert_to_class_list(v)
            elif k.lower() in cls.TEXT_TRANSLATIONS:
                updated_rlvalue[k.lower()] = v
                use_xpath = True
            elif k.lower() == "use_xpath":
                from arjuna.core.types.constants import TRUES, FALSES
                v = str(v).strip()
                if v.lower() not in TRUES and v.lower() not in FALSES:
                    raise Exception("Allowed values for use_path are true/false/on/off")
                if v.lower() in TRUES:
                    use_xpath = True
            else:
                updated_rlvalue[k] = v
        return updated_rlvalue, use_xpath

    @classmethod
    def __translate_node(cls, gltype, rlvalue):
        rlvalue, use_xpath = cls.__process_node_rlvalue_and_xpath_condition(rlvalue)

        if use_xpath:
            return cls.__translate_node_rlvalue_to_xpath(gltype, rlvalue)
        else:
            return cls.__translate_node_to_selector(gltype, rlvalue)

    _NTYPE_GLTYPE_MAP ={
        DomNodeType.NODE: GenericLocateWith.NODE,
        DomNodeType.FNODE: GenericLocateWith.FNODE,
        DomNodeType.BNODE: GenericLocateWith.BNODE,
    }

    _DIRECTION_TO_XPATH_REL_MAP ={
        DomDirection.UP: "/ancestor::",
        DomDirection.DOWN: "/descendant::",
        DomDirection.LEFT: "/preceding-sibling::",
        DomDirection.RIGHT: "/following-sibling::"
    }

    @classmethod
    def __translate_axes(cls, gltype, rlvalue):    
        from arjuna.tpi.helper.arjtype import Node, axes
        def create_xpath_for_part(gltype, locator_value, *, prefix_slashes=False):
            rlvalue, use_xpath = cls.__process_node_rlvalue_and_xpath_condition(locator_value)
            return cls.__translate_node_rlvalue_to_xpath(gltype, rlvalue, prefix_slashes=prefix_slashes)

        xpath_parts = []

        # Process Starting point
        if type(rlvalue) is dict:
            rlvalue = axes._from_dict(rlvalue)
        elif type(rlvalue) is list:
            rlvalue = axes._from_list(rlvalue)
        start = rlvalue._start
        start_gltype = cls._NTYPE_GLTYPE_MAP[start.ntype]
        _, start_rlvalue = create_xpath_for_part(start_gltype, start.as_dict(), prefix_slashes=True)
        xpath_parts.append(start_rlvalue)

        for axis in rlvalue._axes:
            xpath_parts.append(cls._DIRECTION_TO_XPATH_REL_MAP[axis.direction])
            axis_gltype = cls._NTYPE_GLTYPE_MAP[axis.node.ntype]
            _, axis_rlvalue = create_xpath_for_part(axis_gltype, axis.node.as_dict())
            xpath_parts.append(axis_rlvalue)

        return GenericLocateWith.XPATH, "".join(xpath_parts)