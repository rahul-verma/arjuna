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
from .section import GuiSection
from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData

from arjuna import track

@track("debug")
class GuiDialog(GuiSection):
    '''
        Represents a GUI Dialog. Can be associated with a **GuiApp** or **GuiPage**.

        It is an implementation of **GuiAppContent**.

        Args:
            *args: Any number of positional argumnts. These are passed to the **prepare()** method if defined in inherited class.

        Keyword Arguments:
            parent_gui: (Mandatory) The **Gui** object that is associated with this **GuiDialog**.
            label: Label for the this **GuiDialog**. If not provided, the class name is used as the label.
            root: Root element of this **GuiSection**. Can be **label** string defined in its GNS File or a **Locator** object.
            gns_dir: Relative Root Directory for GNS file associated with this **GuiDialog**. Default is **dialog** directory in associated **GuiApp** namespace. If provided, path is considered relative to the **GuiApp** namespace directory.
            gns_file_name: Name of GNS file associated with this **GuiPage**. If not provided, default is **<label>.yaml**.
            kwargs: Arbitrary keyword arugments. These are passed to the **prepare()** method if defined in inherited class.

        Note:
            A **GuiDialog** can have a root element. If defined, all locator calls in this object happen as a nested locating call using the root element.

                - Root element provided in in __init__ call is given preference.
                - If not provided, Arjuna looks for **root** definition in **load** section of its GNS file.
                - If above is also not provided, then locating happens from the root of the DOM of current page.
    '''

    def __init__(self, *args, parent_gui: 'GuiAppOrGuiPage', label: 'str'=None, root: 'LabelOrLocator'=None, gns_dir: str=None, gns_file_name:str=None, **kwargs):
        super().__init__(*args, parent_gui=parent_gui, label=label, root=root, gns_dir=gns_dir, gns_file_name=gns_file_name, **kwargs)



