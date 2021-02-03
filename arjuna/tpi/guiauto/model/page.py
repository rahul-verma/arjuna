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


from .gui import Gui
from .content import GuiAppContent
from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
from arjuna.tpi.tracker import track
from arjuna.tpi.guiauto.source.page import GuiPageSource

@track("debug")
class GuiPage(GuiAppContent):
    '''
        Represents a GUI Page. 
        
        It is an implementation of **GuiAppContent**.

        Args:
            *args: Any number of positional argumnts. These are passed to the **prepare()** method if defined in inherited class.

        Keyword Arguments:
            source_gui: (Mandatory) The **Gui** object from where this **GuiPage** is created. 
            label: Label for the this **GuiPage**. If not provided, the class name is used as the label.
            gns_dir: Relative Root Directory for GNS file(s) associated with this **GuiPage**. Default is **page** directory in associated **GuiApp** namespace. If provided, it is considered relative to the namespace directory of associated **GuiApp**.
            gns_file_name: Name of GNS file associated with this **GuiPage**. If not provided, default is **<label>.yaml**.
            kwargs: Arbitrary keyword arugments. These are passed to the **prepare()** method if defined in inherited class.
    '''


    def __init__(self, *args, source_gui: Gui=None, label: str=None, gns_dir: str=None, gns_file_name: str=None, **kwargs):
        # app = isinstance(source_gui, GuiApp) and source_gui or source_gui.app
        super().__init__(automator=source_gui._automator, label=label, gns_dir=gns_dir, gns_file_name=gns_file_name)
        self.app.ui = self
        from arjuna import ArjunaOption
        if self.config.value(ArjunaOption.BROWSER_NETWORK_RECORDER_AUTOMATIC):
            self._automator.network_recorder.current_title = self.label
        self._load(*args, **kwargs)

    @property
    def source(self) -> GuiPageSource:
        '''
           **GuiPageSource** object for this **Gui**.
        '''
        return self._automator.source
