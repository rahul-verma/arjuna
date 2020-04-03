# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .gui import *
from .page import GuiPage
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData


class _App(Gui, metaclass=abc.ABCMeta):

    def __init__(self, *, config=None, ext_config=None, label=None, gns_dir=None, gns_file_name=None):
        gns_dir = gns_dir is not None and gns_dir or ""
        super().__init__(gns_dir=gns_dir, config=config, ext_config=ext_config, label=label)
        self.__ui = None
        self.__automator = None
        self.__gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.label)

    @property
    def automator(self):
        return self.__automator

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
        self.__ui = GuiPage(source_gui=self, label=self.label, gns_dir=self.gns_dir, gns_file_name=self.__gns_file_name)

    @abc.abstractmethod
    def launch(self):
        pass

    def prepare_widget(self, widget_object):
        return widget_object


class GuiApp(_App):

    def __init__(self, *args, base_url=None, blank_slate=False, config=None, ext_config=None, label=None, gns_dir=None, gns_file_name=None, **kwargs):
        '''
            Creates and returns GuiAutomator object for provided config.
            If no configuration is provided reference configuration is used.
            You can also provide GuiDriverExtendedConfig for extended configuration for WebDriver family of libs. 
        '''
        super().__init__(gns_dir=gns_dir, gns_file_name=gns_file_name, config=config, ext_config=ext_config, label=label is None and self.__class__.__name__ or label)
        from arjuna.tpi.enums import ArjunaOption
        self.__base_url = base_url is not None and base_url or self.config.value(ArjunaOption.APP_URL)
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