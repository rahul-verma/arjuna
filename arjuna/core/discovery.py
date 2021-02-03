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

import os

from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.core.utils import file_utils
from arjuna.core.utils import sys_utils

class DiscoveredFile:
    def __init__(self):
        self.props = {}
        
    def attr(self, attr):
        return self.props[attr]

    def set_attr(self, name, attr):
        self.props[name] = attr


fa_msg1 = '''Duplicate test file found with name: %s.
Check package and class names in test directory.
Arjuna follows a case-INSENSITIVE approach for test names.'''


class FileAggregator:
    def __init__(self):
        self.files = []
        self.found_class_names = set()
        self.temp_map = {}
        from arjuna import Arjuna
        self.logger = Arjuna.get_logger()
        self.console = Arjuna.get_console()

    def add(self, df):
        key = df.attr(DiscoveredFileAttributeEnum.DIRECTORY_ABSOLUTE_PATH) + "/" + df.attr(
            DiscoveredFileAttributeEnum.FULL_NAME).upper()
        if key in self.found_class_names or key in self.temp_map:
            fa_msg1.format(DiscoveredFileAttributeEnum.FULL_NAME)
            self.console.display_error(fa_msg1)
            sys_utils.fexit()
        self.temp_map[key] = df

    def freeze(self):
        paths = []
        paths.extend(self.temp_map.keys())
        paths.sort()
        for path in paths:
            self.files.append(self.temp_map[path])

    def __iter__(self):
        return iter(self.files)

    def enumerate(self):
        for f in self:
            self.logger.debug("-------------------------")
            self.logger.debug("Name:\t" + f.attr(DiscoveredFileAttributeEnum.NAME))
            self.logger.debug("Extension:\t" + f.attr(DiscoveredFileAttributeEnum.EXTENSION))
            self.logger.debug("Full Name:\t" + f.attr(DiscoveredFileAttributeEnum.FULL_NAME))
            self.logger.debug("Package Dot Notation:\t" + f.attr(DiscoveredFileAttributeEnum.PACKAGE_DOT_NOTATION))
            self.logger.debug(
                "Directory Relative Path:\t" + f.attr(DiscoveredFileAttributeEnum.DIRECTORY_RELATIVE_PATH))
            self.logger.debug(
                "Directory Absolute Path:\t" + f.attr(DiscoveredFileAttributeEnum.DIRECTORY_ABSOLUTE_PATH))
            self.logger.debug("Comma Separated Relative Path:\t"
                         + f.attr(DiscoveredFileAttributeEnum.COMMA_SEPATARED_RELATIVE_PATH))
            # self.logger.debug("Container:\t" + f.attr(DiscoveredFileAttributeEnum.CONTAINER))
            # self.logger.debug("Container Type:\t" + f.attr(DiscoveredFileAttributeEnum.CONTAINER_TYPE))
            self.logger.debug("-------------------------")


class FileDiscoverer:
    def __init__(self, aggregator, root_dir, include_prefixes=None):
        self.aggregator = aggregator
        if root_dir.endswith("\\") or root_dir.endswith("//"):
            self.root_dir = root_dir[0:-1]
        else:
            self.root_dir = root_dir
        self.root_dir = file_utils.normalize_path(self.root_dir)
        self.cdir = None
        self.cabsdir = None
        self.prefixes = [file_utils.normalize_path(p) for p in include_prefixes]

    def discover(self):
        for d, subdlist, flist in os.walk(self.root_dir):
            normalized_d = file_utils.normalize_path(d)
            if flist:
                for f in flist:
                    full_path = file_utils.normalize_path(os.path.abspath(os.path.join(normalized_d, f)))
                    consider = False
                    for prefix in self.prefixes:
                        if normalized_d.startswith(prefix):
                            consider = True
                            break
                    if not consider: continue
                    file_ext = file_utils.get_extension(full_path)
                    if file_ext.lower() not in set(['py']): continue
                    parent_dir = file_utils.normalize_path(os.path.dirname(full_path))
                    pkg_parent_dir = None  # os.path.commonpath()
                    if parent_dir == self.root_dir:
                        pkg_parent_dir = ""
                    else:
                        pkg_parent_dir = parent_dir[parent_dir.index(self.root_dir) + len(self.root_dir) + 1:]
                    file_ext = file_utils.get_extension(full_path)

                    df = DiscoveredFile()
                    df.set_attr(DiscoveredFileAttributeEnum.NAME, file_utils.get_nonext_basename(full_path))
                    df.set_attr(DiscoveredFileAttributeEnum.EXTENSION, file_ext)
                    df.set_attr(DiscoveredFileAttributeEnum.FULL_NAME, f)
                    df.set_attr(DiscoveredFileAttributeEnum.PACKAGE_DOT_NOTATION,
                                 pkg_parent_dir.replace("/", "."))
                    df.set_attr(DiscoveredFileAttributeEnum.DIRECTORY_RELATIVE_PATH, pkg_parent_dir)
                    df.set_attr(DiscoveredFileAttributeEnum.DIRECTORY_ABSOLUTE_PATH, parent_dir)
                    replaced = df.attr(DiscoveredFileAttributeEnum.DIRECTORY_RELATIVE_PATH).replace("/", "|")
                    replaced = replaced.replace("\\", "|")
                    df.set_attr(DiscoveredFileAttributeEnum.COMMA_SEPATARED_RELATIVE_PATH,
                                 ",".join(replaced.split("|")))
                    # df.set_attr(DiscoveredFileAttributeEnum.CONTAINER, attr.NA_STRING)
                    # df.set_attr(DiscoveredFileAttributeEnum.CONTAINER_TYPE, attr.NA_STRING)
                    self.aggregator.add(df)

        self.aggregator.freeze()
