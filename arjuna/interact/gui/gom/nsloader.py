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

import re
import os

from enum import Enum, auto
from abc import abstractmethod

from arjuna.core.enums import GuiAutomationContext
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData, Locator, ImplWith

class FileFormat(Enum):
    GNS = auto()
    MGNS = auto()
    XLS = auto()
    XLSX = auto()

class GuiNamespaceLoaderFactory:

    # Returns GuiNamespaceLoader
    @classmethod
    def create_namespace_loader(cls, config, ns_file_path):
        from arjuna.core.enums import ArjunaOption
        multi_context_enabled = config.get_arjuna_option_value(ArjunaOption.GUIAUTO_DEF_MULTICONTEXT).as_bool()
        context = multi_context_enabled and None or config.guiauto_context
        _, file_extension = os.path.splitext(ns_file_path)
        ext = file_extension.upper()[1:]
        considered_path = ns_file_path
        try:
            file_format = FileFormat[ext]
        except:
            raise Exception("Unsupported format for namespace: {}".format(file_extension))
        else:
            full_file_path = ns_file_path
            if os.path.isdir(full_file_path):
                raise Exception("Namespace file path is a directory and not a file: {}".format(considered_path))
            elif not os.path.isfile(full_file_path):
                raise Exception("Namespace file path is invalid: {}".format(considered_path))

            if file_format == FileFormat.GNS:
                if multi_context_enabled:
                    return MGNSFileLoader(full_file_path)
                else:
                    return GNSFileLoader(full_file_path, context)
            else:
                raise Exception("Unsupported format for namespace: {}".format(file_extension))


class GuiNamespace:

    def __init__(self, name):
        self.__name = name
        # dict <string, dict<GuiAutomationContext, GuiElementMetaData>>
        self.__ns = {}

    def add_element_meta_data(self, name, context, raw_locators):
        emd = GuiElementMetaData.create_lmd(*raw_locators)
        #emd = GuiElementMetaData(raw_locators, process_args=False)
        name = name.lower()
        if not self.has(name):
            self.__ns[name] = {}
        self.__ns[name][context] = emd

    def has(self, name):
        return name.lower() in self.__ns

    def has_context(self, name, context):
        if self.has(name):
            return context in self.__ns[name.lower()]
        return False

    # Needs to be thread-safe
    # Returns emd for a context for a given gui name
    def get_meta_data(self, name, context):
        if not self.has(name):
            raise Exception("Gui namespace >{}< does not contain element with name: {}".format(self.__name, name))
        elif not self.has_context(name, context):
            raise Exception("Gui namespace >{}< does not contain element with name: {} for context {}".format(self.__name, name, context))
        
        return self.__ns[name.lower()][context]


class BaseGuiNamespaceLoader:

    def __init__(self, name):
        self.__name = name
        self.__namespace = GuiNamespace(name)

    @property
    def name(self):
        return self.__name

    @property
    def namespace(self):
        return self.__namespace

    # Needs to be thread safe
    def add_element_meta_data(self, name, context, locators):
        self.__namespace.add_element_meta_data(name, context, locators)

    def _raise_notafile_exception(self, file_path):
        raise Exception("{} is not a file.".format(file_path))

    def _raise_filenotfound_exception(self, file_path):
        raise Exception("{} is not a valid file path.".format(file_path))

    def _raise_relativepath_exception(self, file_path):
        raise Exception("Gui namespace loader does not accept relative file path. {} is not a full file path.".format(file_path))

class AbstractGNFileLoader(BaseGuiNamespaceLoader):
    NAME_PATTERN = re.compile(r"\[\s*(.*?)\s*\]$")
    LOCATOR_PATTERN = re.compile(r"\s*(.*?)\s*=\s*(.*?)\s*$")

    def __init__(self, ns_file_path):
        super().__init__(os.path.basename(ns_file_path))
        self.__ns_file = None
        self.__ns_path = None
        self.__header_found = False
        self.__last_header = None
        self.__last_auto_contexts = None # list of auto contexts

        #Map<String, Map<GuiAutomationContext,List<Locator>>>
        self.__ns = {}

        if not os.path.isabs(ns_file_path):
            super()._raise_relativepath_exception(ns_file_path)
        elif not os.path.exists(ns_file_path):
            super()._raise_filenotfound_exception(ns_file_path)
        elif not os.path.isfile(ns_file_path):
            super()._raise_notafile_exception(ns_file_path)

        self.__ns_path = ns_file_path
        self.__ns_file = open(self.__ns_path)

    @property
    def header_found(self):
        return self.__header_found

    @header_found.setter
    def header_found(self, flag):
        self.__header_found = flag

    @property
    def last_header(self):
        return self.__last_header

    @last_header.setter
    def last_header(self, name):
        self.__last_header = name

    @property
    def last_auto_contexts(self):
        return self.__last_auto_contexts

    @last_auto_contexts.setter
    def last_auto_contexts(self, contexts):
        self.__last_auto_contexts = contexts

    @property
    def ns_path(self):
        return self.__ns_path

    @property
    def ns_file(self):
        return self.__ns_file

    def load(self):
        for line in self.__ns_file.readlines():
            line = line.strip()
            if not line: 
                continue
            if self._match_header(line):
                self.header_found = True
                self._init_section()
                continue
            else:
                if not self.header_found:
                    raise Exception("Namespace contents must be contained inside a [name] header.")
                else:
                    self._load_section_line(line)
        
        self.__ns_file.close()

        for ename, context_data in self.__ns.items():
            for context, locators in context_data.items():
                self.add_element_meta_data(ename, context, locators)

    def __is_defined(self, name):
        return name.lower() in self.__ns

    def __is_not_first_header(self):
        return self.last_header is not None

    def __validate_duplicate_entry(self, last_name, new_name):
        if (last_name.lower() == new_name.lower()) or self.__is_defined(new_name):
            raise Exception("Found duplicate namespace definition for {} element.".format(new_name))

    def __validate_empty_last_section(self, name):
        if len(self.__ns[name]) == 0:
            raise Exception("Found empty namespace definition for {} element.".format(name))
        else:
            for context, data in self.__ns[name].items():
                if len(data) == 0:
                    raise Exception("Found empty namespace definition for {} context for {} element.".format(context.name, name))


    def _match_header(self, input):
        match = self.NAME_PATTERN.match(input)
        if match:
            current_header = match.group(1)
            if self.__is_not_first_header():
                self.__validate_duplicate_entry(self.last_header, current_header)
                self.__validate_empty_last_section(self.last_header)
            
            # Initialise for new section found
            self.last_header = current_header
            self.last_auto_contexts = None
            from arjuna.configure.impl.validator import ConfigValidator
            ConfigValidator.arjuna_name(self.last_header)
            self.__ns[self.last_header] = {}
            return True
        else:
            return False

    def _init_contexts_dict(self, name, contexts):
        for context in contexts:
            if context in self.__ns[name]:
                raise Exception("Found duplicate automation context {} in {} namespace definition.".format(context.name, self.last_header))
            else:
                self.__ns[name][context] = []

    @abstractmethod
    def _match_contexts(self, input):
        pass

    @abstractmethod
    def _load_section_line(self, input):
        pass

    @abstractmethod
    def _init_section(self):
        pass

    def _match_locator(self, input):
        match = self.LOCATOR_PATTERN.match(input)
        if match:       
            # locator = Locator(match.group(1), match.group(2), named_args=dict())
            locator = ImplWith(wtype=match.group(1).upper(), wvalue=match.group(2), named_args=dict(), has_content_locator=False)
            # locator = getattr(With, match.group(1).lower())(match.group(2)) # e.g. getattr(With, "ID".lower())("abc")
            if (self.last_auto_contexts is None):
                raise Exception("Locators must be preceded with context information as #context1, context2 construct. Current line: " + input)   

            for context in self.last_auto_contexts:
                self.__ns[self.last_header][context].append(locator)
            return True
        else:
            return False

class GNSFileLoader(AbstractGNFileLoader):

    def __init__(self, ns_file_path, context):
        super().__init__(ns_file_path)
        self.__contexts = [context]

    @property
    def contexts(self):
        return self.__contexts

    def _init_section(self):
        self.last_auto_contexts = self.__contexts
        self._init_contexts_dict(self.last_header, self.contexts)

    def _match_contexts(self, input):
        pass

    def _load_section_line(self, line):
        if self._match_locator(line):
            return
        else:
            raise Exception("Unexpected namespace file entry. Namspace content can either be plaforms or identification definition: " + line)


class MGNSFileLoader(AbstractGNFileLoader):
    PLATFORM_PATTERN = re.compile(r"\s*\#\s*(.*?)\s*$")

    def __init__(self, ns_file_path):
        super().__init__(ns_file_path)

    def _init_section(self):
        pass

    def _match_contexts(self, input):
        match = self.PLATFORM_PATTERN.match(input)
        if match:        
            try:
                raw_contexts = [m.strip().upper() for m in match.group(1).split(",")]
                contexts = [GuiAutomationContext[n] for n in raw_contexts]
            except Exception as e:
                raise Exception("Invalid context name found in header: {}".format(e))
            else:
                self._init_contexts_dict(self.last_header, contexts)
            
            self.last_auto_contexts = contexts
            return True
        else:
            return False

    def _load_section_line(self, line):
        if self._match_contexts(line):
            return
        elif self._match_locator(line):
            return
        else:
            raise Exception("Unexpected namespace file entry. Namspace content can either be plaforms or identification definition: " + line)
