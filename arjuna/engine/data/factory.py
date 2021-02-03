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
from .source import *
from .reference import *
from arjuna.core.utils import file_utils
from arjuna.core.constant import DataRefType

def get_data_file_path(data_dir, fpath):
    if file_utils.is_absolute_path(fpath):
        if not file_utils.is_file(fpath):
            if file_utils.is_dir(fpath):
                raise Exception("Not a file: {}".format(fpath))
            else:
                raise Exception("File does not exist: {}".format(fpath))
        return fpath
    else:
        fpath = os.path.abspath(os.path.join(data_dir, fpath))
        if not file_utils.is_file(fpath):
            if file_utils.is_dir(fpath):
                raise Exception("Not a file: {}".format(fpath))
            else:
                raise Exception("File does not exist: {}".format(fpath))
        return fpath

def create_file_data_source(file_path, *, context, delimiter="\t"):
    from arjuna import Arjuna, ArjunaOption
    data_dir = Arjuna.get_config().value(ArjunaOption.DATA_SRC_DIR)
    file_path = get_data_file_path(data_dir, file_path)
    ds = None
    ext = file_path.lower()
    if ext.endswith(".csv") or ext.endswith(".txt"):
        ds = DsvFileMapDataSource(file_path, delimiter, context=context)
    elif ext.endswith(".xls"):
        ds = ExcelFileMapDataSource(file_path, context=context)
    elif ext.endswith(".ini"):
        ds = IniFileDataSource(file_path, context=context)
    else:
        raise Exception("This is not a default file format supported as a data source: " + file_path)
    return ds

from arjuna.tpi.helper.arjtype import CIStringDict

class DataReferences:

    def __init__(self):
        vars(self)['_store'] = CIStringDict()

    def as_dict(self):
        return vars(self)['_store'].orig_dict

    def __getitem__(self, name):
        return self._store[name]

    def __setitem__(self, name, value):
        self._store[name] = value

    def __getattr__(self, name):
        if type(name) is str and not name.startswith("__"):
            return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self):
        return str(self._store)

    def update(self, data_refs):
        vars(self)['_store'].update(data_refs.as_dict())


class DataReference:

    @classmethod
    def load_all(cls, ref_config):
        from arjuna.tpi.constant import ArjunaOption
        crefs = DataReferences()
        contextual_data_ref_dir = ref_config.value(ArjunaOption.DATA_REF_CONTEXTUAL_DIR)
        if os.path.isdir(contextual_data_ref_dir):
            for fname in os.listdir(contextual_data_ref_dir):
                if not (fname.lower().endswith("xls") or fname.lower().endswith("yaml")) :
                    continue
                crefs[os.path.splitext(fname)[0]] = cls.create_contextual_data_ref(ref_config, fname)

        irefs = DataReferences()
        indexed_data_ref_dir = ref_config.value(ArjunaOption.DATA_REF_INDEXED_DIR)
        if os.path.isdir(indexed_data_ref_dir):
            for fname in os.listdir(indexed_data_ref_dir):
                if not (fname.lower().endswith("xls") or fname.lower().endswith("yaml")) :
                    continue
                irefs[os.path.splitext(fname)[0]] = cls.create_indexed_data_ref(ref_config, fname)
        return crefs, irefs

    @classmethod
    def __create_file_data_ref(cls, ref_config, file_path, type):
        ext = file_path.lower()
        if not ext.endswith("xls") and not ext.endswith("yaml"):
            raise Exception("Unsupported file extension for data reference: {}. Allowed: [xls, yaml]".format(file_path))

        from arjuna import Arjuna, ArjunaOption
        if type == DataRefType.CONTEXTUAL:
            data_dir = ref_config.value(ArjunaOption.DATA_REF_CONTEXTUAL_DIR)
            file_path = get_data_file_path(data_dir, file_path)
            if file_path.lower().endswith("xls"):
                return ExcelContextualDataReference(file_path)
            else:
                return YamlContextualDataReference(file_path)
        elif type == DataRefType.INDEXED:
            data_dir = ref_config.value(ArjunaOption.DATA_REF_INDEXED_DIR)
            file_path = get_data_file_path(data_dir, file_path)
            if file_path.lower().endswith("xls"):
                return ExcelIndexedDataReference(file_path)
            else:
                return YamlIndexedDataReference(file_path)

    @classmethod
    def create_contextual_data_ref(cls, ref_config, file_path):
        return cls.__create_file_data_ref(ref_config, file_path, DataRefType.CONTEXTUAL)

    @classmethod
    def create_indexed_data_ref(cls, ref_config, file_path):
        return cls.__create_file_data_ref(ref_config, file_path, DataRefType.INDEXED)

