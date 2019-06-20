import json
from arjuna.setu.config.processor import ConfigCreator, CentralConfigLoader, ProjectConfigCreator
from arjuna.tpi.enums import ArjunaOption
from arjuna.lib.reader.hocon import HoconStringReader, HoconConfigDictReader

from arjuna.setu.types import SetuManagedObject
from arjuna.setuext.data_broker.databroker import DataBroker


class TestConfigurator:

    def __init__(self):
        self.__default_ref_config = None
        self.__config_map = {}
        self.__cli_central_config = None
        self.__cli_test_config = None

    def __create_config_from_option_dicts(self, reference, arjuna_options, user_options):
        crawdict = {
            "arjunaOptions": arjuna_options,
            "userOptions": user_options
        }
        hreader = HoconStringReader(json.dumps(crawdict))
        hreader.process()
        config = ConfigCreator.create_new_conf(
            self.__default_ref_config.processor,
            reference,
            hreader.get_map()
        )
        return config

    def __init_cli_dicts(self, arjunaCentralOptions={}, arjunaTestOptions={}, userCentralOptions={}, userTestOptions={}):
        self.__cli_central_config = self.__create_config_from_option_dicts(None, arjunaCentralOptions, userCentralOptions)
        self.__cli_test_config = self.__create_config_from_option_dicts(None, arjunaTestOptions,
                                                                        userTestOptions)

    def init(self, root_dir, cli_config):
        self.__default_ref_config = CentralConfigLoader(root_dir).config
        self.__config_map[self.__default_ref_config.setu_id] = self.__default_ref_config
        cli_config = cli_config and cli_config or {}
        self.__init_cli_dicts(**cli_config)
        return self.__default_ref_config.setu_id

    def create_project_conf(self):
        project_conf_loader = ProjectConfigCreator(self.__default_ref_config)
        self.__default_ref_config = project_conf_loader.config
        self.__default_ref_config.process_arjuna_options()
        self.__default_ref_config.update(self.__cli_central_config)
        self.__config_map[self.__default_ref_config.setu_id] = self.__default_ref_config
        return self.__default_ref_config

    def get_central_config(self):
        return self.__default_ref_config

    def get_config(self, setu_id):
        return self.__config_map[setu_id]

    def get_arjuna_option_value(self, config_setu_id, option):
        sname = ArjunaOption[option.upper().strip().replace(".", "_")]
        rvalue = self.__config_map[config_setu_id].setu_config.value(sname)
        return rvalue

    def get_user_option_value(self, config_setu_id, option):
        sname = option.upper().strip().replace(".", "_")
        rvalue = self.__config_map[config_setu_id].user_config.value(sname)
        return rvalue

    def get_central_arjuna_option_value(self, option):
        sname = ArjunaOption[option.upper().strip().replace(".", "_")]
        rvalue = self.__default_ref_config.setu_config.value(sname)
        return rvalue

    def get_central_user_option_value(self, option):
        sname = option.upper().strip().replace(".", "_")
        rvalue = self.__default_ref_config.user_config.value(sname)
        return rvalue

    def register_config(self, arjuna_options, has_parent, user_options, parent_config_id):
        reference = has_parent and self.__config_map[parent_config_id] or self.__default_ref_config
        config = self.__create_config_from_option_dicts(reference, arjuna_options, user_options)
        config.update(self.__cli_test_config)
        config.process_arjuna_options()
        self.__config_map[config.setu_id] = config
        return config


class TestSession(SetuManagedObject):

    def __init__(self):
        super().__init__()
        self.__configurator = TestConfigurator()
        self.__data_broker = DataBroker()

    @property
    def configurator(self):
        return self.__configurator

    @property
    def data_broker(self):
        return self.__data_broker

    def init(self, root_dir, cli_config):
        return self.__configurator.init(root_dir, cli_config)