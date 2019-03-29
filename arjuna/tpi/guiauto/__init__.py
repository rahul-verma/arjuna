from enum import Enum, auto


class _WithType(Enum):
    ID = auto()
    NAME = auto()
    CLASS_NAME = auto()
    LINK_TEXT = auto()
    XPATH = auto()
    CSS_SELECTOR = auto()

    INDEX = auto()
    CHILD_LOCATOR = auto()
    ASSIGNED_NAME = auto()


class With:

    def __init__(self, with_type, with_value):
        '''

        :param with_type: an enum constant of type WithType
        :param with_value: a string or int or a With object.
        '''
        self.__with_type = with_type
        self.__with_value = None
        self.__is_child_locator = False
        self.__child = None

        if with_type == _WithType.CHILD_LOCATOR:
            if not isinstance(with_value, With):
                raise Exception("For identification with child locator, the argument must be a With object.")
            else:
                self.__is_child_locator = True
                self.__child = with_value
        else:
            self.__with_value = with_value


    def as_map(self):
        map = dict()
        map["withType"] = self.__with_type.name
        if not self.__is_child_locator:
            map["withValue"] = self.__with_value
        else:
            map["withValue"] = self.__child.as_map()
        return map

    @staticmethod
    def id(id):
        return With(_WithType.ID, id)

    @staticmethod
    def name(name):
        return With(_WithType.NAME, name)

    @staticmethod
    def class_name(name):
        return With(_WithType.CLASS_NAME, name)

    @staticmethod
    def link_text(text):
        return With(_WithType.LINK_TEXT, text)

    @staticmethod
    def css_selector(selector):
        return With(_WithType.CSS_SELECTOR, selector)

    @staticmethod
    def xpath(xpath):
        return With(_WithType.XPATH, xpath)

    @staticmethod
    def index(index):
        return With(_WithType.INDEX, index)

    @staticmethod
    def child_locator(with_obj):
        return With(_WithType.CHILD_LOCATOR, with_obj)

    @staticmethod
    def assigned_name(name):
        return With(_WithType.ASSIGNED_NAME, name)
