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


class Database(metaclass=abc.ABCMeta):

    def __init__(self, db_handle, config):
        self.__handle = db_handle
        from arjuna import Arjuna
        self.__config = config is not None and config or Arjuna.get_config()

    @property
    def _handle(self):
        return self.__handle

    @property
    def _config(self):
        return self.__config

    def execute_all(self, *queries, merge=True, **formatters):
        cursor = self._handle.cursor()
        if merge:
            queries = ";".join(queries).format(**formatters)
            print(queries)
            cursor.execute(queries, multi=True)
        else:
            for query in queries:
                query = query.format(**formatters)
                print(query)
                cursor.execute(query)

        self._handle.commit()
        cursor.close()

    def __get_sql_file_path(self, fname):
        from arjuna.core.utils import file_utils
        from arjuna import Arjuna, ArjunaOption
        fpath = os.path.abspath(os.path.join(self._config.value(ArjunaOption.DBAUTO_SQL_DIR), fname))
        if file_utils.is_file(fpath):
            return fpath
        else:
            for linked_project in reversed(Arjuna.get_linked_projects()):
                fpath = os.path.abspath(os.path.join(linked_project.ref_conf.value(ArjunaOption.DBAUTO_SQL_DIR), fname))
                if file_utils.is_file(fpath):
                    return fpath
        raise Exception("DBAuto SQL File not found: {}".format(fname))

    def execute_file(self, fpath, **formatters):
        fpath = self.__get_sql_file_path(fpath)
        from arjuna.tpi.parser.text import TextFileAsLines
        reader = TextFileAsLines(fpath)
        queries = list()
        for query in reader:
            if query != "":
                queries.append(query)
        return self.execute_all(*queries, **formatters)

    def close(self):
        self._handle.close()


class MySQL(Database):

    def __init__(self, db_handle, config):
        super().__init__(db_handle, config)


class DB:

    @classmethod
    def mysql(cls, *, host, user, password, port=3306, config=None):
        import mysql.connector
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            ssl_disabled = True,

        )
        return MySQL(db, config)


