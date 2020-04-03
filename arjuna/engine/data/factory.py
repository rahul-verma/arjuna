# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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
from arjuna.tpi.enums import DataRefContextType

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

def create_file_data_source(file_path, record_format="MAP", delimiter="\t"):
    from arjuna import Arjuna, ArjunaOption
    data_dir = Arjuna.get_config().value(ArjunaOption.DATA_SRC_DIR)
    file_path = get_data_file_path(data_dir, file_path)
    ds = None
    ext = file_path.lower()
    rformat = record_format.upper()
    if ext.endswith(".csv") or ext.endswith(".txt"):
        if rformat == "LIST":
            ds = DsvFileListDataSource(file_path, delimiter)
        else:
            ds = DsvFileMapDataSource(file_path, delimiter)
    elif ext.endswith(".xls"):
        if rformat == "LIST":
            ds = ExcelFileListDataSource(file_path)
        else:
            ds = ExcelFileMapDataSource(file_path)
    elif ext.endswith(".ini"):
        ds = IniFileDataSource(file_path)
    else:
        raise Exception("This is not a default file format supported as a data source: " + path)
    return ds

from arjuna.tpi.helpers.types import CIStringDict

class DataReferences:

    def __init__(self):
        vars(self)['_store'] = CIStringDict()

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

class DataReference:

    @classmethod
    def load_all(cls, ref_config):
        from arjuna.tpi.enums import ArjunaOption
        refs = DataReferences()
        column_data_ref_dir = ref_config.value(ArjunaOption.DATA_REF_COLUMN_DIR)
        for fname in os.listdir(column_data_ref_dir):
            if fname.lower().endswith("xls"):
                refs[os.path.splitext(fname)[0]] = DataReference.create_excel_column_data_ref(fname)
        
        row_data_ref_dir = ref_config.value(ArjunaOption.DATA_REF_ROW_DIR)
        for fname in os.listdir(row_data_ref_dir):
            if fname.lower().endswith("xls"):
                refs[os.path.splitext(fname)[0]] = DataReference.create_excel_row_data_ref(fname)

        return refs

    @classmethod
    def __create_excel_file_data_ref(cls, file_path, context=DataRefContextType.COLUMN):
        ext = file_path.lower()
        if not ext.endswith("xls"):
            raise Exception("Unsupported file extension for Excel data reference: {}".format(file_path))

        from arjuna import Arjuna, ArjunaOption
        if context == DataRefContextType.COLUMN:
            data_dir = Arjuna.get_config().value(ArjunaOption.DATA_REF_COLUMN_DIR)
            file_path = get_data_file_path(data_dir, file_path)
            return ExcelColumnDataReference(file_path)
        elif context == DataRefContextType.ROW:
            data_dir = Arjuna.get_config().value(ArjunaOption.DATA_REF_ROW_DIR)
            file_path = get_data_file_path(data_dir, file_path)
            return ExcelRowDataReference(file_path)

    @classmethod
    def create_excel_column_data_ref(cls, file_path):
        return cls.__create_excel_file_data_ref(file_path, context=DataRefContextType.COLUMN)

    @classmethod
    def create_excel_row_data_ref(cls, file_path):
        return cls.__create_excel_file_data_ref(file_path, context=DataRefContextType.ROW)

