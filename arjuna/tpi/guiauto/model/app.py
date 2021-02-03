# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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
from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
from arjuna.tpi.tracker import track
from arjuna.tpi.log import *

@track("debug")
class _App(Gui, metaclass=abc.ABCMeta):

    def __init__(self, *, config=None, ext_config=None, label=None, gns_dir=None, gns_file_name=None):
        gns_dir = gns_dir is not None and gns_dir or ""
        super().__init__(gns_dir=gns_dir, config=config, ext_config=ext_config, label=label)
        self.__ui = None
        self.__automator = None
        self.__gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.label)
        self.__common_gui_def = None

    @property
    def _automator(self):
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

    @property
    def _common_guidef(self):
        return self.__common_gui_def

    def _create_default_ui(self):
        self.__ui = GuiPage(source_gui=self, label=self.label, gns_dir=self.gns_dir, gns_file_name=self.__gns_file_name)
        self.__common_gui_def = self.__ui._gui_def

    @abc.abstractmethod
    def launch(self):
        pass

    def prepare_widget(self, widget_object):
        return widget_object

@track("debug")
class GuiApp(_App):
    '''
        Represents a GUI App.

        It supports all methods of **GuiAppContent** by delegating to a default **GuiPage** which it encapsulates.

        Args:
            *args: Any number of positional argumnts. These are passed to the **prepare()** method if defined in inherited class.

        Keyword Arguments:
            url: Base URL for Web application. If not provided, value of **ArjunaOption.APP_URL** is taken from the associated **Configuration** object.
            config: Configuration object.
            ext_config: (Not Supported Yet) AutomatorExtendedConfig object for underlying GUI automator.
            label: Label for the GuiApp. If not provided, the class name is used as the label.
            gns_dir: Relative Root Directory for GNS file(s) associated with the GuiApp. Default is **<ProjectRootDirectory>/guiauto/namespace**. If provided, it is considered relative to the namespace directory.
            gns_file_name: Name of GNS file associated with GuiApp. If not provided, default is **<label>.yaml**.
            kwargs: Arbitrary keyword arugments. These are passed to the **prepare()** method if defined in inherited class.

        Note:
            GuiApp can be used as singular represenation of complete page.

            Through its advanced Python implementation, **GuiApp** supports all methods that are supported by a **GuiPage** by delegating the calls to an internal page object.

            So, although not directly visible in the API docs for GuiApp, you can call all **GuiPage** methods on **GuiApp** as well and they will be executed on the current page in the browser.
    '''

    def __init__(self, *args, url: str=None, config: 'Configuration'=None, ext_config: 'AutomatorExtendedConfig'=None, label: str=None, gns_dir: str=None, gns_file_name: str=None, **kwargs):
        super().__init__(gns_dir=gns_dir, gns_file_name=gns_file_name, config=config, ext_config=ext_config, label=label is None and self.__class__.__name__ or label)
        from arjuna.tpi.constant import ArjunaOption
        self.__url = url is not None and url or self.config.value(ArjunaOption.APP_URL)
        # self._load(*args, **kwargs)
        self.__args = args
        self.__kwargs = kwargs

    @property
    def url(self):
        '''
            Base URL of this GuiApp
        '''
        return self.__url

    def launch(self, *, blank_slate=False):
        '''
            Launch GuiApp.

            Keyword Arguments:
                blank_state: If True, App's base URL is not opened. Default is False.
        '''
        self._launchautomator()
        if self.config.value(ArjunaOption.BROWSER_NETWORK_RECORDER_AUTOMATIC):
            self._automator.network_recorder.record(title=self.__class__.__name__ + " - Home")
        if not blank_slate:
            self._automator.browser.go_to_url(self.url)
        self._create_default_ui()
        self._load(*self.__args, **self.__kwargs)

    def quit(self):
        '''
            Close browser and do cleanup of GuiApp.
        '''
        try:
            if self.config.value(ArjunaOption.BROWSER_NETWORK_RECORDER_AUTOMATIC):
                self._automator.network_recorder.register()
        except:
            pass
        self._automator.quit()

    def __getattr__(self, name):
        return getattr(self.ui, name)

    @property
    def main_window(self):
        '''
           Main window of this **GuiApp**
        '''
        return self._automator.main_window

    def child_window(self, *str_or_with_locators):
        '''
            (Not Supported Yet) Child Window.
        '''
        return self._automator.child_window(self.convert_to_with_wmd(*str_or_with_locators))

    @property
    def latest_child_window(self):
        '''
            (Not Supported Yet) Latest Child Window.
        '''
        return self._automator.latest_child_window

    def close_all_child_windows(self):
        '''
            (Not Supported Yet) Close All Child Windows
        '''
        self._automator.close_all_child_windows()