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
import platform
import abc
from enum import Enum
import tempfile

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.constant import ArjunaOption
from arjuna.tpi.parser.yaml import Yaml
from arjuna.tpi.error import DisallowedArjunaOptionError, ArjunaOptionValidationError
from .validator import Validator
from .stage import ConfigStageKeys
from arjuna.core.constant import ConfigStage
from enum import Enum
from arjuna.tpi.constant import BrowserName

class Options(metaclass=abc.ABCMeta):

    def __init__(self, *, options_dict, creation_context, validate=True):
        self.__options = CIStringDict()
        self.__validate = validate
        if options_dict:
            self.update_all(options_dict)

    def update(self, option_name, option_value):
        option_name = self._process_option_name(option_name)
        validator_name = "not_fetched_yet"
        try:
            is_not_set = False
            try:
                is_not_set = option_value.lower() == "not_set"
            except:
                pass
            finally:
                option_key = self.__get_option_key(option_name)
                if is_not_set:
                    self.__options[option_key] = "not_set"
                else:
                    validator_name, validator = self._get_validator_for(option_name)
                    if self.__validate:
                        self.__options[option_key] = validator(option_value)
                    else:
                        if validator_name.lower() not in {'absolute_dir_path', 'absolute_file_path'}:
                            self.__options[option_key] = validator(option_value)
                        else:
                            self.__options[option_key] = option_value
        except Exception as e:
            raise ArjunaOptionValidationError(option_value, option_name, validator_name, str(e))
    
    def __get_option_key(self, option_name):
        return isinstance(option_name, Enum) and option_name.name or option_name

    @abc.abstractmethod
    def _process_option_name(self, option_name):
        pass

    @abc.abstractmethod
    def _get_validator_for(self, option_name):
        pass

    def value(self, option_name):
        return self.__options[self.__get_option_key(self._process_option_name(option_name))]

    def update_all(self, options):
        if isinstance(options, Options):
            self.__options.update(options.as_dict())
        else:
            if options:
                for k,v in options.items():
                    self.update(k,v)

    def as_dict(self):
        return self.__options

    def is_not_set(self, option_name):
        self._process_option_name(option_name)
        try:
            return self.value(option_name).upper() == "NOT_SET"
        except:
            return False

class ArjunaOptions(Options):

    ARJUNA_OPTIONS_DESC_MAP = None

    @classmethod
    def process_arjuna_option_name(cls, name):
        try:
            if not isinstance(name, ArjunaOption):
                return ArjunaOption[UserOptions.process_option_name(name)]
            else:
                return name
        except Exception as e:
            raise Exception("Config option <{}> is not a valid ArjunaOption constant".format(name))

    @classmethod
    def load_desc(cls):
        if cls.ARJUNA_OPTIONS_DESC_MAP is not None:
            return
        my_dir = os.path.dirname(os.path.realpath(__file__))
        desc_file = os.path.abspath(os.path.join(my_dir, "..", "res", "arjuna_conf_desc.yaml"))
        creation_context=f"This Yaml represents arjuna_conf_desc.yaml configuration file at {desc_file} that describes rules for Arjuna's built-in options."
        desc_yaml = Yaml.from_file(desc_file)
        cls.ARJUNA_OPTIONS_DESC_MAP = {cls.process_arjuna_option_name(k): v for k, v in desc_yaml.as_map().items()}

    def __init__(self, *, options_dict, creation_context, validate=True):
        super().__init__(options_dict=options_dict, creation_context=creation_context, validate=validate)

    def _get_validator_for(self, option_name):
        validator_name = self.ARJUNA_OPTIONS_DESC_MAP[option_name]
        return validator_name, getattr(Validator, validator_name.lower())

    def _process_option_name(self, option_name):
        return self.process_arjuna_option_name(option_name)

    def __modify_bin_name_for_windows(self, name):
        if platform.system().lower() == "windows":
            return name + ".exe"
        else:
            return name

    def __get_driver_path(self, name):
        existing_driver_path = self.value(ArjunaOption.SELENIUM_DRIVER_PATH)
        not_set_yet_str = "$driver_name$"
        if existing_driver_path.find(not_set_yet_str) != -1:
            return self.value(ArjunaOption.SELENIUM_DRIVER_PATH).replace(not_set_yet_str, self.__modify_bin_name_for_windows(name))
        else:
            # Some other driver might have been set
            return os.path.join(os.path.dirname(existing_driver_path), name)

    def process_options(self):
        for_browser = {
            BrowserName.CHROME: {
                ArjunaOption.SELENIUM_DRIVER_PROP : "webdriver.chrome.driver",
                ArjunaOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("chromedriver")
            },

            BrowserName.FIREFOX: {
                ArjunaOption.SELENIUM_DRIVER_PROP : "webdriver.gecko.driver",
                ArjunaOption.SELENIUM_DRIVER_PATH : self.__get_driver_path("geckodriver")
            }
        }

        browser = self.get_browser_name()
        self.update_all(for_browser[browser])

    def get_browser_name(self):
        return self.value(ArjunaOption.BROWSER_NAME)

class UserOptions(Options):

    def __init__(self, *, options_dict, creation_context):
        super().__init__(options_dict=options_dict, creation_context=creation_context)

    @classmethod
    def process_option_name(cls, name):
        try:
            if isinstance(name, Enum):
                return name.name.upper()
            else:
                return name.upper().strip().replace(".", "_")
        except Exception as e:
            raise Exception("An error occured in processing Config option <{}> as a user option. Error: {}".format(name, str(e)))

    @classmethod
    def pass_through(cls, input):
        return input

    def _get_validator_for(self, option_name):
        return "pass_through", self.pass_through

    def _process_option_name(self, option_name):
        return self.process_option_name(option_name)

class EditableConfig:
    _OS_MAP = {
        'Windows': 'windows',
        'Darwin': 'mac',
        'Linux': 'linux'
    }

    def __init__(self, *, arjuna_options_dict, user_options_dict, creation_context, validate=True):
        self.__arjuna_options = ArjunaOptions(options_dict=arjuna_options_dict, creation_context=creation_context, validate=validate)
        self.__user_options = UserOptions(options_dict=user_options_dict, creation_context=creation_context)

    @property
    def arjuna_options(self):
        return self.__arjuna_options

    @property
    def user_options(self):
        return self.__user_options

    def as_dict(self):
        return {
            'arjuna_options': self.arjuna_options.as_dict(),
            'user_options': self.user_options.as_dict()
        }


    def update(self, conf):
        self.__arjuna_options.update_all(conf.arjuna_options)
        self.__user_options.update_all(conf.user_options)

    def update_from_maps(self, *, arjuna_options, user_options):
        self.__arjuna_options.update_all(arjuna_options)
        self.__user_options.update_all(user_options)

    def process_arjuna_options(self):
        self.__arjuna_options.process_options()

    def set_arjuna_option(self, arjuna_option, obj):
        self.__arjuna_options.update(arjuna_option, obj)

    def set_user_option(self, option, obj):
        self.__user_options.update(option, obj)

    def set_option(self, option, obj):
        try:
            self.set_arjuna_option(option, obj)
        except DisallowedArjunaOptionError:
            raise
        except ArjunaOptionValidationError:
            raise
        except Exception as e:
            self.set_user_option(option, obj)
        return self

    def add_options(self, options):
        for option, obj in options.items():
            self.set_option(option, obj)
        return self

    def is_empty(self):
        if not self.arjuna_options and not self.user_options:
            return True
        return False

    @classmethod
    def validate_arjuna_options_for_stage(cls, stage, options):
        if isinstance(options, ArjunaOptions):
            options = options.as_dict()
        for option in options:
            ConfigStageKeys.validate(stage, UserOptions.process_option_name(option))

    @classmethod
    def empty_conf(cls):
       return EditableConfig(arjuna_options_dict=None, user_options_dict=None, creation_context="")

    @classmethod
    def from_file(cls, *, file_path, creation_context, conf_stage, validate=True, **replacements):
        with open(file_path, "r") as f:
            return cls.from_str(contents=f.read(), creation_context=creation_context, conf_stage=conf_stage, validate=validate, **replacements)

    @classmethod
    def from_str(cls, *, contents, creation_context, conf_stage, validate=True, **replacements):
        for rname, rvalue in replacements.items():
            contents = contents.replace("${}$".format(rname), rvalue)

        if not contents:
            return EditableConfig(
            arjuna_options_dict = dict(),
            user_options_dict = dict(),
            creation_context = "This configuration represents " + creation_context,
            )
        
        contents_yaml = Yaml.from_str(contents)

        return cls.from_yaml(yaml_obj=contents_yaml, creation_context=creation_context, conf_stage=conf_stage, validate=validate)

    @classmethod
    def from_yaml(cls, *, yaml_obj, creation_context, conf_stage, validate=True):
        arjuna_options_dict = yaml_obj.get_section("arjuna_options", strict=False, allow_any=True)
        if arjuna_options_dict is not None:
            arjuna_options_dict = arjuna_options_dict.as_map()
        else:
            arjuna_options_dict = dict()        
        user_options_dict = yaml_obj.get_section("user_options", strict=False, allow_any=True)
        if user_options_dict is not None:
            user_options_dict = user_options_dict.as_map()
        else:
            user_options_dict = dict()

        if conf_stage != ConfigStage.DEFAULT:
            cls.validate_arjuna_options_for_stage(conf_stage, arjuna_options_dict)

        return EditableConfig(
            arjuna_options_dict = arjuna_options_dict,
            user_options_dict = user_options_dict,
            creation_context = "This configuration represents " + creation_context,
            validate=validate
        )

    @classmethod
    def arjuna_conf(cls, *, project_root_dir, run_id):
        my_dir = os.path.dirname(os.path.realpath(__file__))
        location = os.path.abspath(os.path.join(my_dir, "..", "res", "arjuna.yaml"))
        return cls.from_file(
            file_path=location,
            creation_context=f"arjuna.yaml default configuration file at {location}",
            conf_stage=ConfigStage.DEFAULT,
            arjuna_root_dir = os.path.abspath(os.path.join(my_dir, "..", "..")),
            project_root_dir = project_root_dir,
            project_name = os.path.basename(project_root_dir),
            host_os = cls._OS_MAP[platform.system()],
            run_id = run_id and run_id or "mrun",
            # temp_dir = tempfile.TemporaryDirectory().name,
            validate=False
        )

    @classmethod
    def project_conf(cls, *, arjuna_conf, linked_projects):
        proj_conf = cls.empty_conf()
        for linked_project in linked_projects:
            proj_conf.update(linked_project.ref_conf_editable)
        proj_conf.update(arjuna_conf)
        location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_PROJECT_LOCAL_FILE)
        if not os.path.isfile(location):
            location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_PROJECT_FILE)
        if not os.path.isfile(location):
            return proj_conf
        proj_conf.update(
            cls.from_file(
                file_path = location,
                creation_context = f"project.yaml configuration file at {location}",
                conf_stage=ConfigStage.PROJECT,
            )
        )
        return proj_conf

    @classmethod
    def from_maps(cls, *, conf_stage, ref_config, arjuna_options, user_options):
        conf = cls.empty_conf()
        if ref_config: conf.update(ref_config)     
        if arjuna_options:
            cls.validate_arjuna_options_for_stage(conf_stage, arjuna_options)
        conf.update_from_maps(arjuna_options=arjuna_options, user_options=user_options)
        return conf

    @classmethod
    def __multi_confs_file(cls, *, file_path, creation_context):
        yaml = Yaml.from_file(file_path, allow_any=True)
        conf_map = dict()
        if yaml is not None:
            for section_name in yaml.section_names:
                conf_map[section_name] = cls.from_yaml(yaml_obj=yaml.get_section(section_name), creation_context=f"Section {section_name} in {creation_context}", conf_stage=ConfigStage.REFERENCE)

        return conf_map


    @classmethod
    def data_confs(cls, *, arjuna_conf):
        location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_DATA_LOCAL_FILE)
        if not os.path.isfile(location):        
            location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_DATA_FILE)
        if not os.path.isfile(location):
            return {}
        return cls.__multi_confs_file(
            file_path=location, creation_context=f"Data Configuration file at {location}"
        )

    @classmethod
    def env_confs(cls, *, arjuna_conf):
        location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_ENVS_LOCAL_FILE)
        if not os.path.isfile(location):  
            location = arjuna_conf.arjuna_options.value(ArjunaOption.CONF_ENVS_FILE)
        if not os.path.isfile(location):
            return {}
        return cls.__multi_confs_file(
            file_path=location, creation_context=f"Environment Configuration file at {location}"
        )
