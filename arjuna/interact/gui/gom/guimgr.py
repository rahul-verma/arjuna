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

import uuid
from arjuna.interact.gui.gom.namestore import GuiNameStore
from arjuna.tpi.constant import ArjunaOption

class GuiManager:

    def __init__(self, config):
        self.__name_store = GuiNameStore()
        self.__namespace_dir = config.arjuna_options.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)

    @property
    def name_store(self):
        return self.__name_store

    @property
    def namespace_dir(self):
        return self.__namespace_dir

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        from arjuna.interact.gui.gom.guidef import GuiDef
        gui_def = GuiDef(self.__name_store, self.__namespace_dir, automator, label, def_file_path)
        gui = Gui(self, automator, gui_def)
        return gui


