from arjuna.setu.types import SetuManagedObject
from arjuna.setuext.guiauto.impl.element.guielement import GuiElement
from arjuna.tpi.enums import ArjunaOption

class BasicWindow(SetuManagedObject):

    def __init__(self, automator):
        super().__init__()
        self.__automator = automator
        self.__window_handle = None
        self.__config = automator.config

    @property
    def config(self):
        return self.__config    

    @property
    def automator(self):
        return self.__automator

    @property
    def handle(self):
        return self.__window_handle

    def _set_handle(self, handle):
        self.__window_handle = handle

    def focus(self):
        self.automator.dispatcher.focus_on_window(self.handle)

    def is_main_window(self):
        return False

    def set_window_size(self, width, height):
        self.automator.dispatcher.set_current_window_size(width, height)

    def maximize(self):
        self.automator.dispatcher.maximize_current_window()

    def get_title(self):
        return self.automator.dispatcher.get_current_window_title()

    def get_size(self):
        return self.automator.dispatcher.get_current_window_size()

class MainWindow(BasicWindow):

    def __init__(self, automator):
        super().__init__(automator)
        self._set_handle(self.get_current_window_handle()) 
        self.__all_child_windows = {}
        self.__setu_id_map = {}
        self.__resize_window_as_per_config()

    def get_all_child_window_handles(self):
        handles = self.automator.dispatcher.get_all_window_handles()
        handles = [handle for handle in handles if handle != self.handle]
        new_handles = []
        for handle in handles:
            if handle != self.handle:
                if handle not in self.__all_child_windows:
                    cwin = ChildWindow(self.automator, self, handle)
                    self.__all_child_windows[handle] = cwin
                    self.__setu_id_map[cwin.setu_id] = cwin
                    new_handles.append(handle)
        return handles, new_handles

    def get_latest_child_window(self):
        _, new_handles = self.get_all_child_window_handles()
        if not new_handles:
            raise Exception("No new window was launched.")
        elif len(new_handles) > 1:
            raise Exception("Multiple new windows were launched, so can not deterministically jump to a new window.")
        return self.__all_child_windows[new_handles[0]]

    def __get_child_window(self, handle):
        return self.__all_child_windows[handle]

    def __focus_on_window(self, handle):
        self.__get_child_window(handle).jump()

    def delete_window(self, setu_id, handle):
        del self.__all_child_windows[handle]
        del self.__setu_id_map[setu_id]

    def close_all_child_windows(self):
        all_child_handles, _ = self.get_all_child_window_handles()
        for handle in all_child_handles:
            cwin = self.__get_child_window(handle)
            cwin.focus()
            cwin.close()
        self.focus()

    def get_current_window_handle(self):
        return self.automator.dispatcher.get_current_window_handle()

    def get_window_for_setu_id(self, setu_id):
        if self.setu_id == setu_id:
            return self
        else:
            return self.__setu_id_map[setu_id]

    def get_window_for_locator(self, locator_type, locator_value):
        all_child_handles, _ = self.get_all_child_window_handles()
        for handle in all_child_handles:
            cwin = self.__get_child_window(handle)
            cwin.focus()
            if locator_type.lower() == "window_title":
                if cwin.get_title() == locator_value:
                    return cwin
                else:
                    try:
                        element = self.automator.create_element_with_locator(locator_type, locator_value)
                        element.find()
                        return cwin
                    except:
                        continue
        raise Exception("No child window contains an element with locator type: {} and locator value: {}".format(locator_type, locator_value))

    def __resize_window_as_per_config(self):
        # Resize window
        config = self.config
        browser_width = config.setu_config.value(ArjunaOption.BROWSER_DIM_WIDTH)
        browser_height = config.setu_config.value(ArjunaOption.BROWSER_DIM_HEIGHT)
        should_maximize = config.setu_config.value(ArjunaOption.BROWSER_MAXIMIZE)

        if config.setu_config.is_not_set(ArjunaOption.BROWSER_DIM_WIDTH) and config.setu_config.is_not_set(ArjunaOption.BROWSER_DIM_HEIGHT):
            if should_maximize:
                self.maximize()
        else:
            width, height = None, None
            current_width, current_height = self.get_size()
            width = config.setu_config.is_not_set(ArjunaOption.BROWSER_DIM_WIDTH) and browser_width or current_width
            height = config.setu_config.is_not_set(ArjunaOption.BROWSER_DIM_HEIGHT) and browser_height or current_height
            self.set_window_size(width, height)

    def is_main_window(self):
        return True

    def close(self):
        raise Exception("You can not close main window. Use automator.quit() to quit application.")

class ChildWindow(BasicWindow):

    def __init__(self, automator, main_window, handle):
        super().__init__(automator)
        self.__main_window = main_window
        self._set_handle(handle) 

    def close(self):
        self.focus()
        self.automator.dispatcher.close_current_window()
        self.__main_window.delete_window(self.setu_id, self.handle)
        self.__main_window.focus()