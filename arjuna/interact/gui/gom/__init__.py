'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from .gui import *
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData

class Page(AppContent):

    def __init__(self, *args, source_gui, label=None, **kwargs):
        # app = isinstance(source_gui, App) and source_gui or source_gui.app
        super().__init__(automator=source_gui.automator, label=label)
        self.app.ui = self
        self._load(*args, **kwargs)

class Section(AppContent):

    def __init__(self, gui, *args, root_element_locators=None, label=None, **kwargs):
        super().__init__(automator=gui.automator, label=label)   
        self.__root_element_locators = root_element_locators
        self.__root_element = None
        self._load(*args, **kwargs)
        self.__parent = gui

    def load_root_element(self):
        gns_re_locators = None
        coded_re_locators = None
        # From GUI Def
        if self.externalized:
            gns_re_locators = self.gui_def.root_element_with_locators

        # From constructor. Overrides Gui Def if both places have the def.        
        if self.__root_element_locators is not None:
            if type(self.__root_element_locators) not in {list, tuple}:
                self.__root_element_locators = (self.__root_element_locators,)
            coded_re_locators = self.__root_element_locators

        self.__root_element_locators = self.__root_element_locators and coded_re_locators or coded_re_locators or gns_re_locators

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Loaded Root Element for {} widget. Loaded as: {}. Externalized: {}. RE locators in GNS: {}. RE in __init__: {}.".format(
            self.label,
            GuiElementMetaData.locators_as_str(self.__root_element_locators),
            self.externalized,
            GuiElementMetaData.locators_as_str(gns_re_locators),
            GuiElementMetaData.locators_as_str(coded_re_locators)
        ))

        if self.__root_element_locators is not None:
            self.__root_element = super().element(*self.__root_element_locators)

    @property
    def root(self):
        return self.__root_element

    def element(self, *str_or_with_locators, iconfig=None):
        if self.root:
            return self.root.element(*str_or_with_locators, iconfig=iconfig)
        else:
            return super().element(*str_or_with_locators, iconfig=iconfig)

    def multi_element(self, *str_or_with_locators, iconfig=None):
        return self.automator.multi_element(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    @property
    def parent(self):
        return self.__parent

Widget = Section
Dialog = Section

class App(Gui, metaclass=abc.ABCMeta):

    def __init__(self, *, config=None, ext_config=None, label=None, gns_dir=None):
        super().__init__(config=config, ext_config=ext_config, label=label)
        self.__ui = None
        self.__automator = None
        self.__gns_dir = gns_dir

    @property
    def automator(self):
        return self.__automator

    @property
    def gns_dir(self):
        return self.__gns_dir

    @gns_dir.setter
    def gns_dir(self, d):
        self.__gns_dir = d

    def _launchautomator(self):
        # Default Gui automation engine is Selenium
        from arjuna.interact.gui.auto.automator import GuiAutomator
        self.__automator = GuiAutomator(self, self.config, self.ext_config)    

    @property
    def ui(self):
        return self.__ui

    @ui.setter
    def ui(self, page):
        self.__ui = page

    def _create_default_ui(self):
        self.__ui = Page(source_gui=self, label="{}-Def-UI".format(self.label))

    @abc.abstractmethod
    def launch(self):
        pass

    def prepare_widget(self, widget_object):
        return widget_object


class WebApp(App):

    def __init__(self, *args, base_url=None, blank_slate=False, config=None, ext_config=None, label=None, gns_dir=None, **kwargs):
        '''
            Creates and returns GuiAutomator object for provided config.
            If no configuration is provided reference configuration is used.
            You can also provide GuiDriverExtendedConfig for extended configuration for WebDriver family of libs. 
        '''
        super().__init__(config=config, ext_config=ext_config, label=label, gns_dir=gns_dir)
        from arjuna.core.enums import ArjunaOption
        self.__base_url = base_url is not None and base_url or self.config.arjuna_options.value(ArjunaOption.AUT_BASE_URL)
        # self._load(*args, **kwargs)
        self.__args = args
        self.__kwargs = kwargs

    @property
    def base_url(self):
        return self.__base_url

    def launch(self, blank_slate=False):
        self._launchautomator()
        if not blank_slate:
            self.automator.browser.go_to_url(self.base_url)
        self._create_default_ui()
        self._load(*self.__args, **self.__kwargs)

    def quit(self):
        self.automator.quit()

    def __getattr__(self, name):
        return getattr(self.ui, name)

    def externalize(self, *, gns_dir=None, gns_file_name=None):
        self.__gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.label)        
        from arjuna.core.enums import ArjunaOption   
        self.gns_dir = gns_dir and gns_dir or self.gns_dir
        if not self.gns_dir:
            self.gns_dir = ""
        self.ui.externalize(gns_dir=self.gns_dir, gns_file_name=self.__gns_file_name)
        self._set_externalized()