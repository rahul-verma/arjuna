class TestSessionDataBrokerHandler:

    def __init__(self, testsession_handler, data_broker):
        self.__data_broker = data_broker
        self.__testsession_handler = testsession_handler

    def take_action(self, action_type, json_dict):
        return getattr(self, action_type.name.lower())(**json_dict) 

    def create_file_data_source(self, fileName, recordType, **json_dict):
        data_dir = self.__testsession_handler.conf_handler.configurator.get_central_arjuna_option_value(ArjunaOption.DATA_SOURCES_DIR.name)
        return {"dataSourceSetuId" : self.__data_broker.create_file_data_source(data_dir, fileName, recordType, **json_dict)}  

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