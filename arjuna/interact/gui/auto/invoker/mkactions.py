from enum import Enum, auto

class PartialActionType(Enum):
    CLICK = auto()
    CLICK_AND_HOLD = auto()
    MOUSE_UP = auto()
    RIGHT_CLICK = auto()
    DOUBLE_CLICK = auto()
    DRAG_AND_DROP = auto()
    SEND_KEYS = auto()
    MOVE_TO = auto()
    PAUSE = auto()

class DefaultCompositeAction:

    def __init__(self, automator, partial_actions):
        self.__partial_actions = partial_actions
        self.__automator =  automator

    def perform(self):
        self.__automator.perform_composite_action(self)

    @property
    def partial_actions(self):
        return self.__actions


class PartialAction:

    def __init__(self, action_type):
        self.__type = action_type
        self.__args = dict()

    def add_target_gui_element(self, element):
        args["target_element"] = element

    def add_source_element(self, element):
        args["source_element"] = element

    def add_target_point(self, point):
        args["target_point"] = point

    def add_source_point(self, point):
        args["source_point"] = point

    def add_offset(self, offset):
        args["offset"] = offset

    def add_key_chord(self, chord):
        args["chord"] = chord

    def add_pause_time(self, t):
        args["pause"] = t

    @property
    def action_type(self):
        return self.__type

    @property
    def args(self):
        return self.__args


class SingleActionChain:

    def __init__(self, automator):
        self.__automator = automator
        self.__actions = list()

    def __default_action_chain(partial_action_type):
        action = PartialAction(partial_action_type)
        self.__actions.append(action)

    def __default_point_action(partial_action_type, point):
        action = PartialAction(partial_action_type)
        action.add_target_point(point)
        self.__actions.append(action)
        return self

    def __default_element_action(partial_action_type, element):
        action = PartialAction(partial_action_type)
        action.add_target_guielement(element)
        self.__actions.append(action)
        return self

    def __click_action(self, *, atype, point, element):
        if point is None:
            if element is None:
                return self.__default_action_chain(PartialActionType.DOUBLE_CLICK)
            else:
                self.__default_element_action(PartialActionType.DOUBLE_CLICK, element)
        else:
            if element is None:
                return self.__default_point_action(PartialActionType.DOUBLE_CLICK, point)
            else:
                raise Exception("You can not provide both point and element to {} action.".format(atype))

    def release(self):
        return self.__default_action_chain(PartialActionType.MOUSE_UP)

    def click(self, *, point=None, element=None):
        return self.__click_action(PartialActionType.CLICK, point, element)

    def press(self, *, point=None, element=None):
        return self.__click_action(PartialActionType.CLICK_AND_HOLD, point, element)

    def right_click(self, *, point=None, element=None):
        return self.__click_action(PartialActionType.RIGHT_CLICK, point, element)

    def double_click(self, *, point=None, element=None):
        return self.__click_action(PartialActionType.DOUBLE_CLICK, point, element)

    def drag_and_drop(self, *, source_element=None, source_point=None, dest_element=None, dest_point=None, offset=None):
        action = PartialAction(PartialActionType.DRAG_AND_DROP)
        if source_element is not None: action.add_source_element(source_element)
        if source_point is not None: action.add_source_point(source_point)
        if dest_element is not None: action.add_target_point(dest)
        if offset is not None: action.add_offset(xy)
        if dest_point is not None: action.add_target_point(dest_point)
        self.__actions.append(action)
        return self

    def send_text(self, text, *modifier_keys):
        return self

    def send_keys(self, key_chord=None):
        return self

    def hover(self, *, dest_element=None, dest_point=None, offset=None):
        action = PartialAction(PartialActionType.MOVE_TO)
        if dest is not None: action.add_target_gui_element(dest_element)
        if offset is not None: action.add_offset(offset)
        if dest_point is not None: action.add_target_point(dest_point)
        self.__actions.append(action)

    def pause(self, duration):
        action = PartialAction(PartialActionType.PAUSE)
        action.add_pause_time(duration)
        self.__actions.append(action)
        return self

    def build(self):
        return DefaultCompositeAction(self.__automator, self.__actions)

    def perform(self):
        action = this.build()
        action.perform()


class SingleActionChainBuilder:

    def chain(self):
        pass

    def build(self):
        pass

    def perform(self):
        pass