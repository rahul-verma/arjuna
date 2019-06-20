import re
import os

from enum import Enum, auto

from arjuna.tpi.enums import GuiAutomationContext
from arjuna.setuext.guiauto.impl.locator.emd import GuiElementMetaData, Locator

class FileFormat(Enum):
    GNS = auto()
    XLS = auto()
    XLSX = auto()

class GuiNamespaceLoaderFactory:

    # Returns GuiNamespaceLoader
    @classmethod
    def create_namespace_loader(cls, ns_file_path):
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
                return NamespaceFileLoader(full_file_path)
            else:
                raise Exception("Unsupported format for namespace: {}".format(file_extension))


class GuiNamespace:

    def __init__(self, name):
        self.__name = name
        # dict <string, dict<GuiAutomationContext, GuiElementMetaData>>
        self.__ns = {}

    def add_element_meta_data(self, name, context, raw_locators):
        emd = GuiElementMetaData(raw_locators)
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


class NamespaceFileLoader(BaseGuiNamespaceLoader):

    def __init__(self, ns_file_path):
        super().__init__(os.path.basename(ns_file_path))
        self.__ns_file = None
        self.__ns_path = None
        self.name_pattern = re.compile(r"\[\s*(.*?)\s*\]$")
        self.platform_pattern = re.compile(r"\s*\#\s*(.*?)\s*$")
        self.locator_pattern = re.compile(r"\s*(.*?)\s*=\s*(.*?)\s*$")
        self.header_found = False
        self.last_header = None
        self.last_auto_contexts = None # list of auto contexts
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

    def __match_header(self, input):
        match = self.name_pattern.match(input)
        if match:
            current_header = match.group(1)
            if not self.last_header:
                self.last_header = current_header
            elif self.last_header.lower() == current_header.lower():
                raise Exception("Found duplicate namespace definition for {} element.".format(self.last_header))
            else:
                if len(self.__ns[self.last_header]) == 0:
                    raise Exception("Found empty namespace definition for {} element.".format(self.last_header))
                else:
                    for context, data in self.__ns[self.last_header].items():
                        if len(data) == 0:
                            raise Exception("Found empty namespace definition for {} context for {} element.".format(context.name, self.last_header))
                self.last_header = current_header

            self.last_auto_contexts = None
            self.__ns[self.last_header] = {}
            return True
        else:
            return False

    def __match_contexts(self, input):
        match = self.platform_pattern.match(input)
        if match:        
            try:
                raw_contexts = [m.strip().upper() for m in match.group(1).split(",")]
                contexts = [GuiAutomationContext[n] for n in raw_contexts]
            except Exception as e:
                raise Exception("Invalid context name found in header: {}".format(e))
            else:
                for context in contexts:
                    if context in self.__ns[self.last_header]:
                        raise Exception("Found duplicate automation context {} in {} namespace definition.".format(context.name, self.last_header))
                    else:
                        self.__ns[self.last_header][context] = []
            
            self.last_auto_contexts = contexts
            return True
        else:
            return False

    def __match_locator(self, input):
        match = self.locator_pattern.match(input)
        if match:       
            locator = Locator(match.group(1), match.group(2))
            if (self.last_auto_contexts is None):
                raise Exception("Locators must be preceded with context information as #context1, context2 construct. Current line: " + input)   

            for context in self.last_auto_contexts:
                self.__ns[self.last_header][context].append(locator)
            return True
        else:
            return False

    def load(self):
        for line in self.__ns_file.readlines():
            line = line.strip()
            if not line: 
                continue
            if self.__match_header(line):
                self.header_found = True
                continue
            else:
                if not self.header_found:
                    raise Exception("Namespace contents must be contained inside a [name] header.")
                elif self.__match_contexts(line):
                    continue
                elif self.__match_locator(line):
                    continue
                else:
                    raise Exception("Unexpected namespace file entry. Namspace content can either be plaforms or identification definition: " + line)
        
        self.__ns_file.close()

        for ename, context_data in self.__ns.items():
            for context, locators in context_data.items():
                self.add_element_meta_data(ename, context, locators)