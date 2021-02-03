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

class GuiNameStore:

    def __init__(self):
        # dict<String, GuiNameStore>
        self.__ns_map = {}

    # Needs to be thread safe
    def has_namespace(self, name):
        return name in self.__ns_map

    # loader is GuiNamespaceLoader
    # Needs to be thread safe
    def load_namespace(self, name, loader):
        if not self.has_namespace(name):
            loader.load()
            self.__ns_map[name.lower()] = loader.namespace

        return self.__ns_map[name.lower()]

    # Needs to be thread-safe
    def get_namespace(self, name):
        return self.__ns_map[name.lower()]