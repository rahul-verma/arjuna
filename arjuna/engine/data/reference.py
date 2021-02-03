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
import abc

from arjuna.core.reader.excel import *
from arjuna.tpi.data.record import *
from arjuna.tpi.parser.yaml import Yaml

from arjuna.tpi.data.reference import IndexedDataReference, ContextualDataReference

class ExcelIndexedDataReference(IndexedDataReference):

    def __init__(self, path):
        self.path = path
        self.__name = get_file_name(path)
        if (path.lower().endswith("xls")):
            self.reader = ExcelRow2MapReader(path)
        else:
            raise Exception("Unsupported file format for Excel reading.")

        map = dict()
        for index, record in enumerate(self.reader):
            map[index] = DataRecord(context="Ref-{}[{}]".format(self.__name, index), **record)
        self.reader.close()
        super().__init__(map)

class YamlIndexedDataReference(IndexedDataReference):

    def __init__(self, path):
        self.path = path
        self.__name = get_file_name(path)
        if (path.lower().endswith("yaml")):
            self.__node = Yaml.from_file(path)
        else:
            raise Exception("Unsupported file format for Excel reading.")

        map = dict()
        for index, record in enumerate(self.__node):
            map[index] = DataRecord(context="Ref-{}[{}]".format(self.__name, index), **dict(record.items()))
        super().__init__(map)

def get_file_name(path):
    name = os.path.basename(path)
    return os.path.splitext(name)[0]

class YamlContextualDataReference(ContextualDataReference):

    def __init__(self, path):
        if (path.lower().endswith("yaml")):
            self.__node = Yaml.from_file(path)
        else:
            raise Exception("Unsupported file format for Excel reading.")
        super().__init__(path)

    def _populate(self):
        for context in self.__node:
            self._add_record(context, dict(self.__node.get_section(context).items()))


class __ExcelDataReference(ContextualDataReference):
    def __init__(self, path):
        if (path.lower().endswith("xls")):
            self.reader = ExcelRow2ArrayReader(path)
        else:
            raise Exception("Unsupported file format for Excel reading.")
        super().__init__(path)

    @abc.abstractmethod
    def _populate(self):
        pass

class ExcelContextualDataReference(__ExcelDataReference):

    def __init__(self, path):
        super().__init__(path)

    def _populate(self):
        contexts = self.reader.headers[1:]
        cmap = {i: {} for i in contexts}
        while True:
            try:
                data_record = self.reader.next()
            except StopIteration:
                break
            else:
                name = data_record[0]
                for index, context in enumerate(contexts):
                    cmap[context][name] = data_record[index+1]
        self.reader.close()
        for context, value in cmap.items():
            self._add_record(context, value)

def R(query="", *, bucket=None, context=None, index=None):
    if context is not None and index is not None:
        raise Exception("You can either specify context (for contextual references) or index (for indexed references).")
    from arjuna import Arjuna, ArjunaOption
    bucket = bucket
    context = context
    index = index
    query = query

    final_query = ""

    bucket = bucket is not None and bucket.lower() + "." or "."
    context_or_index = None
    if context is not None:
        context_or_index = context.lower() + "."
    elif index is not None:
        context_or_index = str(index) + "."
    else:
        context_or_index = "."

    final_query = bucket + context_or_index + query.lower().strip()
    final_query = final_query.replace("..",".")
    if final_query.startswith('.'):
        final_query = final_query[1:]

    if final_query.endswith('.'):
        final_query = final_query[:-1]

    try:
        bucket, context_or_index, query = final_query.split('.', 2)
    except ValueError:
        query = ""
        try:
            bucket, context_or_index = final_query.split('.', 1)
        except:
            context_or_index = ""
            try:
                bucket = final_query
            except:
                raise Exception("Not able to form a valid reference query with provided data. Invalid query: {}".format(final_query))

    try:
        context_or_index = int(context_or_index)
    except:
        if context_or_index == "":
            context_or_index = None

    try:
        query = int(query)
    except:
        if query == "":
            query = None

    try:
        if context_or_index is not None:
            if query is None:
                return Arjuna.get_data_ref(bucket)._record_for(context_or_index)
            else:
                return Arjuna.get_data_ref(bucket)._record_for(context_or_index)[query]
        else:
            return Arjuna.get_data_ref(bucket)
    except Exception as e:
        import traceback
        raise Exception("Error in retrieving reference value for: bucket: >>{}<<, context: >>{}<< and query >>{}<< in data reference. {}. {}".format(bucket, context, query, str(e), traceback.format_exc()))


    # if bucket is not None:
    #     bucket = bucket.lower()
    #     if context is not None:
    #         context = context.lower()
    #         query = query.lower()
    #     else:
    #         if query.find('.') != -1:
    #             context, query = query.split('.', 1)
    #             context = context.lower()
    #             query = query.lower()
    #         else:
    #             raise Exception("DataRefError: The query must specify context using dot notation when not passed as argument.")
    # else:
    #     if context is not None:
    #         raise Exception("bucket must be provided if context arg is passed.")
    #     else:
    #         if query.find('.') != -1:
    #             bucket, context, query = query.split('.', 2)
    #             bucket = bucket.lower()
    #             context = context.lower()
    #             query = query.lower()
    #         else:
    #             raise Exception("DataRefError: The query must specify bucket and context using dot notation when these are not passed as arguments.")           



