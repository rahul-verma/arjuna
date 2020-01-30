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

# Skeleton. needs to be ported.

class ArjunaSingleton:

    def __init__(self):
        self.__DEFAULT_CONTEXT_NAME = "default_context"
        self.__root_dir = None
        self.__test_session = test_session
        self.__ref_config = None
        self.__cli_config = None
        self.__logger = None
        self.__test_context_map = dict()

    def init(self, root_dir=None):
        self.__root_dir = root_dir
        self.__cli_config = CliArgsConfig()
        # Finalize logger
        createLogger("arjuna", rootDir + File.separator + "log" + File.separator + "arjuna-java.log")
        logger = Logger.getLogger("arjuna")
        Console.init()

        self.__test_session = DefaultTestSession()
        self.__ref_config = self.__test_session.init(root_dir)

        context = this.createTestContext(self.__DEFAULT_CONTEXT_NAME)
        self.__test_session[self.__DEFAULT_CONTEXT_NAME] = context
        return context

    @property
    def cli_config(self):
        return self.__cli_config

    @property
    def ref_config(self):
        return self.__ref_config

    @property
    def root_dir(self):
        return self.__root_dir

    def register_test_context(self, context):
        self.__test_context_map[context.name.lower()] = context

    def get_test_context(name):
        if name is None:
            raise Exception("Context name was passed as None.")
        try:
            return self.__test_context_map[name.lower()]
        except:
            raise Exception("No context found with name: " + name)

    def create_test_context(name):
        return DefaultTestContext(self.__test_session, name)

    def normalize_user_option(self, option):
        return option.strip().upper().replace(".", "_")

    def normalize_arjuna_option(self, option):
        return ArjunaOption[self.normalize_user_option(option)]

    def create_data_source_builder(self):
        return DataSourceBuilder(self.__test_session)

    def create_gui_automator(self, config=None, extended_config=None):
        return DefaultGuiAutomator(config and config or self.__ref_config, extended_config)

    def create_logger(self, logger_name, log_file_path):
        pass