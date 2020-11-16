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
    def translate(cls, locator):
        from arjuna import log_debug

        def process_selector(cssvalue):
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

        def convert_to_class_list(cssvalue):
            return process_selector(cssvalue)[1:].split(".")

        def process_tags(tagsvalue):
            tag_list = None
            if type(tagsvalue) is str:
                tag_list = tagsvalue.strip().split()
            else:
                tag_list = tagsvalue
            return [t.lower()=='any' and '*' or t for t in tag_list]

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
                css_string = process_selector(rlvalue)
                # if type(rlvalue) is str:
                #     css_string = "." + rlvalue.replace('.', ' ').strip()
                # else:
                #     if type(rlvalue[0]) is str:
                #         css_string = "." + rlvalue[0].replace('.', ' ').strip()
                #     else:
                #         css_string = "." + ".".join(rlvalue[0])
                glvalue = process_selector(rlvalue)
                gltype = GenericLocateWith.CSS_SELECTOR
            elif gltype == GenericLocateWith.TAGS:
                glvalue = " ".join(process_tags(rlvalue))
                gltype = GenericLocateWith.CSS_SELECTOR                
            elif gltype in {GenericLocateWith.NODE, GenericLocateWith.BNODE, GenericLocateWith.FNODE}:
                lkeys = [k.lower() for k in rlvalue.keys()]
                if 'tag' in lkeys and 'tags' in lkeys:
                    raise Exception("node Locator definition can contain either 'tag' or 'tags' a key.")
                if len(set(lkeys).intersection(set(cls.TEXT_TRANSLATIONS.keys()))) > 1:
                    raise Exception("node Locator definition can contain only one of text/star_text/*text/dot_text/.text keys.")
                # Initial processing
                updated_rlvalue = dict()
                use_xpath = False
                for k,v in rlvalue.items():
                    if k.lower() == 'tag':
                        updated_rlvalue['tags'] = process_tags(v)
                    elif k.lower() == 'tags':
                        updated_rlvalue['tags'] = process_tags(v)
                    elif k.lower() == 'classes':
                        updated_rlvalue['classes'] = convert_to_class_list(v)
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
                rlvalue = updated_rlvalue
                if use_xpath:
                    # Create XPath
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
                    glvalue = f"//{tags}{xblocks_str}"
                    gltype = GenericLocateWith.XPATH
                else:
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
            else:
                raise Exception("Locator not supported yet by Arjuna: " + rltype)
    
        return GuiGenericLocator(gltype, glvalue)