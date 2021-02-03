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

import sqlite3


class BaseDB:
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def drop_table(self, table_name):
        try:
            self.cursor.execute("DROP TABLE %s" % table_name)
        except:
            pass

    def execute(self, sql):
        # print self.cursor
        results = self.cursor.execute(sql)
        return results

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
