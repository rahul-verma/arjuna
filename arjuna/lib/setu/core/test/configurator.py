import json
from arjuna.lib.setu.core.config.processor import ConfigCreator, CentralConfigLoader, ProjectConfigCreator
from arjuna.tpi.enums import ArjunaOption
from arjuna.lib.trishanku.tpi.reader.hocon import HoconStringReader, HoconConfigDictReader

class TestConfigurator:
    
    def __init__(self):
        self.__default_ref_config = None 
        self.__config_map = {}

    def init(self, root_dir):
        self.__default_ref_config = CentralConfigLoader(root_dir).config
        self.__config_map[self.__default_ref_config.setu_id] = self.__default_ref_config
        return self.__default_ref_config.setu_id

    def create_project_conf(self):
        project_conf_loader = ProjectConfigCreator(self.__default_ref_config)
        self.__default_ref_config = project_conf_loader.config
        self.__default_ref_config.process_setu_options()
        self.__config_map[self.__default_ref_config.setu_id] = self.__default_ref_config
        return self.__default_ref_config.setu_id

    def get_central_config(self):
        return self.__default_ref_config

    def get_config(self, setu_id):
        return self.__config_map[setu_id]

    def get_setu_option_value(self, config_setu_id, option):
        sname = ArjunaOption[option.upper().strip().replace(".","_")]
        rvalue = self.__config_map[config_setu_id].setu_config.value(sname)
        return rvalue

    def get_central_setu_option_value(self, option):
        sname = ArjunaOption[option.upper().strip().replace(".","_")]
        rvalue = self.__default_ref_config.setu_config.value(sname)
        return rvalue

    def register_config(self, setu_options, has_parent, user_options, parent_config_id):
        ref = has_parent and self.__config_map[parent_config_id] or self.__default_ref_config
        crawdict = {
                "setuOptions" : setu_options,
                "userOptions" : user_options
        }
        hreader = HoconStringReader(json.dumps(crawdict))
        hreader.process()
        config = ConfigCreator.create_new_conf(
            self.__default_ref_config.processor, 
            ref,
            hreader.get_map()
        )
        config.process_setu_options()
        self.__config_map[config.setu_id] = config
        return config.setu_id


    
