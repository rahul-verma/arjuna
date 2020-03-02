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

import os
from .source import *

def create_file_data_source(file_path, record_format="MAP", delimiter="\t"):
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
