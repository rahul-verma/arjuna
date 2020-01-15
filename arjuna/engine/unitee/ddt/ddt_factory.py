'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

from .source import *
from .reference import *

def create_ds(path, delimiter="\t"):
    ext = path.lower()
    if ext.endswith(".csv"):
        return DsvFileDataSource(path, ",")
    elif ext.endswith(".txt"):
        return DsvFileDataSource(path, delimiter)
    elif ext.endswith(".xls"):
        return ExcelFileDataSource(path);
    elif ext.endswith(".ini"):
        return IniFileDataSource(path);
    else:
        raise Exception("This is not a default file format supported as a data source: " + path)

def create_dref(path, key=None):
    ext = path.lower()
    if ext.ends_with(".xls"):
        return ExcelDataReference(path, key);
    else:
        raise Exception("Unsupported file reference: " + path)
