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

class TestSessionDataBrokerHandler:

    def __init__(self, testsession_handler, data_broker):
        self.__data_broker = data_broker
        self.__testsession_handler = testsession_handler

    def take_action(self, action_type, json_dict):
        return getattr(self, action_type.name.lower())(**json_dict) 

    def create_file_data_source(self, fileName, recordType, context="Test", **json_dict):
        data_dir = self.__testsession_handler.conf_handler.configurator.get_central_arjuna_option_value(ArjunaOption.DATA_SRC_DIR.name)
        return {"dataSourceSetuId" : self.__data_broker.create_file_data_source(data_dir, fileName, recordType, context=context, **json_dict)}  

    def get_next_record(self, sourceSetuId):
        try:
            return {"finished" : False, "record" : self.__data_broker.get_next_record(sourceSetuId)}
        except Exception:
            return {"finished" : True}

    def get_all_records(self, sourceSetuId):
        try:
            return {"records" : self.__data_broker.get_all_records(sourceSetuId)}
        except Exception:
            return {"finished" : True}

    def reset(self, sourceSetuId):
        return {"finished" : False, "record" : self.__data_broker.reset(sourceSetuId)}