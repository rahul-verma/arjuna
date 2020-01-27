from arjuna import Page

from .widgets import *

class WPBasePage(Page):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.externalize_guidef()


class WPFullPage(WPBasePage):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.__top_nav = self.app.prepare_widget(TopNavBar(self))
        self.__left_nav = self.app.prepare_widget(LeftNavSideBar(self))

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav

