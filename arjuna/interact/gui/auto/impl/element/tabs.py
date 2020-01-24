from .base_element import ElementConfig

class Tab:

    def __init__(self, automator, label_elem, content_relation_attr, content_relation_type):
        super().__init__(automator, parent)
        self.__label_elem = label_elem
        self.__tab_group = tab_group
        self.__label = label_elem.text

        # Find an element based on content of attribute that ties a tab label to content that it controls.
        attr_value = label_elem.get_attr_value(content_relation_attr)
        with_obj = getattr(With, content_relation_type.name.lower())(attr_value)

        self.__tab_content_lmd = self.automator.create_lmd(with_obj)
        self.__tab_content = None

    @property
    def label(self):
        return self.__name

    def click(self):
        self.__label_elem.click()
        self.__tab_content = self.__tab_grouptab_group.root.element(self.__tab_content_lmd)

    def element(self, *with_locators):
        self.__content.element(*with_locators)


class TabGroup(ElementConfig):

    def __init__(self, automator, emd, *, tab_header_lmd, content_relation_attr, content_relation_type, parent=None):
        super().__init__(automator)
        self.__root = automator.define_element(emd)
        tabs = self.root.define_element(tab_header_lmd).identify()
        self.__tabs = []
        for i in range(tabs.length):
            self.__tabs.append(Tab(self, tabs.at_index(i), content_relation_attr, content_relation_type))

    @property
    def root(self):
        return self.__root

    @property
    def labels(self):
        return [t.label for t in self.__tabs]
