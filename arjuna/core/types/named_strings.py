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

from arjuna.tpi.error import *
from arjuna.core.error import *

class NamedString:
    def __init__(self, internal, external):
        self.code = internal
        self.name = external

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name


class NamedStringsContainer:
    def __init__(self, name):
        self.container_name = name
        self.names = []

    def add(self, name):
        self.names.append(name)

    def get_name(self):
        return self.container_name

    def get_named_strings(self):
        return self.names


class Name(NamedString):
    pass


class Message(NamedString):
    pass


class NamesContainer(NamedStringsContainer):
    pass


class MessagesContainer(NamedStringsContainer):
    pass


def populate_from_codelist(map, codes):
    for index, code in enumerate(codes):
        map[code[0].upper().trim()] = code[2]


def populate_from_codemap(map, codes):
    for k, v in codes:
        map[k.upper()] = v


def populate_from_namedstringlist(map, named_strings):
    for ns in named_strings:
        map[ns.get_code().upper()] = ns.get_name()


class StringsManager:
    def __init__(self):
        self.msg_map = {}
        self.name_map = {}
        self.prop_map = {}
        self.flattened_names = {}

    def populate_names(self, names_containers_list):
        for nc in names_containers_list:
            if nc.get_name() not in self.name_map:
                self.name_map[nc.get_name()] = {}
            populate_from_namedstringlist(self.name_map[nc.get_name()], nc.get_named_strings())

    def populate_messages(self, messages_containers_list):
        for mc in messages_containers_list:
            if mc.get_name() not in self.msg_map:
                self.msg_map[mc.get_name()] = {}
            populate_from_namedstringlist(self.msg_map[mc.get_name()], mc.get_named_strings())

    def populate_flattened_names(self):
        for section in self.name_map:
            for key in self.name_map[section]:
                self.flattened_names[section + "::" + key] = self.name_map[section][key]

    def get_all_names(self):
        return self.name_map

    def get_all_messages(self):
        return self.msg_map;

    def get_flattneded_names(self):
        return self.flattened_names;

    def __section_exists(self, section):
        return section in self.msg_map

    def __code_exists(self, section, code):
        if not self.__section_exists(section):
            return False;
        return code in self.msg_map[section]

    def __throw_not_initialized_exception(self, context, method):
        raise Problem("adv", context, method, "LOCALIZER_NOT_INITIALIZED",
                      "Strings Manager not initialized.")

    def __get_text_for_code(self, section, msg_code):
        section_code = section.to_upper_case().trim();
        code = msg_code.to_upper_case().trim();
        if not self.__code_exists(section_code, code):
            return code;
        return self.msg_map[section_code][code]

    def get_info_message_text(self, msg_code):
        return self.__get_text_for_code("INFO_MESSAGES", msg_code)

    def get_problem_text(self, msg_code):
        return self.__get_text_for_code("PROBLEM_MESSAGES", msg_code)

    def get_warning_text(self, msg_code):
        return self.__get_text_for_code("WARNING_MESSAGES", msg_code);

    def get_configured_name(self, section_name, internal_name):
        return self.name_map[section_name.to_upper_case().trim()][internal_name.to_upper_case().trim()]

    class problem_codes:
        pass

    class info_codes:
        pass

    class error_codes:
        pass

    def add_property_name(self, prop_code, prop_name):
        self.prop_map[prop_code.upper()] = prop_name

    def get_property_name(self, prop_code):
        return self.prop_map[prop_code.upper()]
