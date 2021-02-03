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

###############################
# Raised by top layer user API
###############################

'''
Arjuna Exceptions

This module defines Exception classes that represent different types of run-time issues that can happen. The exceptions encapsulate the underlying exception message and stack traces.
'''

import threading

from arjuna.core.error import *
from arjuna.core.utils.obj_utils import get_function_meta_data

class UndefinedConfigError(Exception):
    '''
        Raised when a configurtion is a referenced by its name in code, externalized files or configuration query.
    '''

    def __init__(self, referred_conf_name, defined_conf_names):
        super().__init__("There is no registered configuration for name: {}. Registered: {}".format(referred_conf_name, tuple(defined_conf_names)))

class ConfigCreationError(Exception):
    '''
        Raised when there is an error in the creation of a configuration object.
    '''

    def __init__(self, msg):
        super().__init__(msg)


class GuiWidgetForLabelPresentError(Exception):
    '''
        Raised when a GuiWidget corresponding to a GNS label is unexpectedly found. Involves Dynamic Waiting for absence.
    '''

    def __init__(self, gui, label, message=None):
        message = format_msg(message)
        super().__init__("GuiWidget corresponding to Label {} in Gui {} is present despite waiting.{}".format(label, gui.label, message))


class GuiWidgetPresentError(Exception):
    '''
        Raised when a GuiWidget is unexpectedly found using a GuiWidgetDefinition object. Involves Dynamic Waiting for absence.
    '''

    def __init__(self, gui, wmd, message=None):
        message = format_msg(message)
        super().__init__("GuiWidget corresponding to meta data {} in Gui {} is present despite waiting.{}".format(str(wmd), gui.label, message))

class GuiWidgetForLabelNotPresentError(Exception):
    '''
        Raised when a GuiWidget corresponding to a GNS label is NOT found. Involves Dynamic Waiting for presence.
    '''

    def __init__(self, gui, label, message=None):
        message = format_msg(message)
        super().__init__("GuiWidget corresponding to Label {} in Gui {} is NOT present despite waiting.{}".format(label, gui.label, message))


class GuiWidgetNotPresentError(Exception):
    '''
        Raised when a GuiWidget is NOT found using a GuiWidgetDefinition object. Involves Dynamic Waiting for presence.
    '''

    def __init__(self, gui, wmd, message=None):
        message = format_msg(message)
        super().__init__("GuiWidget corresponding to meta data {} in Gui {} is NOT present despite waiting.{}".format(str(wmd), gui.label, message))


class GuiNamespaceLoadingError(Exception):
    '''
        Raised when there is a problem with loading a GNS file.
    '''

    def __init__(self, gui, msg):
        message = msg and  " Error message: {}".format(msg) or ""
        super().__init__("Gui namespace was not loaded for >{}<.{}".format(gui.qual_name, message))


class GuiNotLoadedError(WaitableError):
    '''
        Raised when there is a problem at any step of Arjuna's Gui Loading Protocol.
    '''

    def __init__(self, gui, msg):
        message = msg and  " Error message: {}.".format(msg) or ""
        super().__init__("GUI [{}] did not load as expected.{}".format(gui.qual_name, message))


class GuiLabelNotPresentError(Exception):
    '''
        Raised when a non-existing GNS label is referenced.
    '''

    def __init__(self, gns_name, label, context=None, msg=None):
        msg = msg is None and "" or msg
        context_msg = context and  " for context {}".format(context) or ""
        super().__init__("Gui namespace >{}< does not contain element with name: {}{}. {}.".format(gns_name, label, context_msg, msg))


class GuiLabelNotPresentError(Exception):
    '''
        Raised when a non-existing GNS label is referenced.
    '''

    def __init__(self, gns_name, label, context=None, msg=None):
        msg = msg is None and "" or msg
        context_msg = context and  " for context {}".format(context) or ""
        super().__init__("Gui namespace >{}< does not contain element with name: {}{}. {}.".format(gns_name, label, context_msg, msg))


class GuiWidgetDefinitionError(Exception):
    '''
        Raised when there is a problem in the way GuiWidgetDefinition is specified in the arguments.
    '''

    def __init__(self, msg):
        super().__init__(msg)


class TestSessionsFileNotFoundError(Exception):
    '''
        Raised when `run-session` CLI sommand is used and sessions.yaml does not exist in `<Project Root Dir>/config` directory.
    '''

    def __init__(self, *, file_path):
        super().__init__(f"Test sessions configuration file does not exist at {file_path}.")


class UndefinedTestSessionError(Exception):
    '''
        Raised when there is no definition for a name used as test session name.
    '''

    def __init__(self, *, name, file_path):
        super().__init__(f"No session definition exists for name >>{name}<< in sessions configuration file at {file_path}.")

class InvalidTestSessionDefError(Exception):
    '''
        Raised when there is an error in the definition of a test session.
    '''

    def __init__(self, *, session_name, sessions_file_path, msg):
        super().__init__(f"Invalid session definition for >>{session_name}<< in sessions file {sessions_file_path}. {msg}")

class TestStagesFileNotFoundError(Exception):
    '''
        Raised when there `run-session/run-stage` CLI sommand is used and stages.yaml is does not exist in `<Project Root Dir>/config` directory.
    '''

    def __init__(self, *, file_path):
        super().__init__(f"Test Stages configuration file does not exist at {file_path}.")

class UndefinedTestStageError(Exception):
    '''
        Raised when there is no definition for a name used as test stage name.
    '''

    def __init__(self, *, name, file_path):
        super().__init__(f"No stage definition exists for name >>{name}<< in stages configuration file at {file_path}")


class InvalidTestStageDefError(Exception):
    '''
        Raised when there is an error in the definition of a test stage.
    '''

    def __init__(self, *, session_name, stage_name, stages_file_path, msg):
        super().__init__(f"Invalid stage definition for >>{stage_name}<< in stages file {stages_file_path}. It is referred in session >>{session_name}<<. {msg}")

class TestGroupsFileNotFoundError(Exception):
    '''
        Raised when there `run-session/run-stage/run-group` CLI sommand is used and `groups.yaml` does not exist at `<Project Root Dir>/config` directory.
    '''

    def __init__(self, *, file_path):
        super().__init__(f"Test groups configuration file does not exist at {file_path}.")

class UndefinedTestGroupError(Exception):
    '''
        Raised when there is no definition for a name used as test group name.
    '''

    def __init__(self, *, name, file_path):
        super().__init__(f"No group definition exists for name >>{name}<< in groups configuration file at {file_path}")

class TestSelectorNotFoundError(Exception):
    '''
        Test Selector object was not found for current thread (and for current test group creation.)

        Every Test Group is run in a thread either sequentially or parallely.

        A Test Selector object is supposed to be created for every test group.

        This exception is raised when Arjuna is not able to find the registered test Selector object for current thread.
    '''

    def __init__(self):
        super().__init__("No test Selector object was found for current test group in thread: {}".format(threading.current_thread().name))


class TestDecoratorError(Exception):
    '''
        Raised when there is an error in @test decorator for a given test function.
    '''

    def __init__(self, func_qual_name, msg):
        super().__init__(f"There is an error in @test decoratior for {func_qual_name}. {msg}")


class HttpUnexpectedStatusCodeError(Exception):
    '''
        Raised when the HTTP status code for a request does not match expected status code(s).
    '''

    def __init__(self, request, response):
        super().__init__(f"Unexpected status code {response.status_code} for {response.url} in {request.method} request.")
        self.__request = request
        self.__response = response

    @property
    def request(self):
        return self.__request

    @property
    def response(self):
        return self.__response

class HttpRequestCreationError(Exception):
    '''
    Raised when there is an error in creating an HTTP request.
    '''

    def __init__(self, msg):
        super().__init__(f"Error in creating HTTP Request. {msg}")

class HttpConnectError(Exception):
    '''
    Raised when there is a connection error.
    '''

    def __init__(self, request, msg):
        super().__init__(f"Connection Error: {request.method} {request.url}. {msg}")
        self.__request = request

    @property
    def request(self):
        return self.__request


class HttpSendError(Exception):
    '''
        Raised when there is an error in sending an HTTP request.
    '''

    def __init__(self, request, response, msg):
        super().__init__(f"Error in HTTP Request: {request.method} {request.url}. {msg}")
        self.__request = request
        self.__response = response

    @property
    def request(self):
        return self.__request

    @property
    def response(self):
        return self.__response

class DisallowedArjunaOptionError(Exception):
    '''
        Raised when there is an attempt to set an ArjunOption value in a configuration stage, where it is not allowed to override the value.
    '''

    def __init__(self, stage, option):
        super().__init__("Option {} is not allowed in a {} configuration.".format(option, stage.name.title()))


class ArjunaOptionValidationError(Exception):

    def __init__(self, option, name, validator, emsg=None):
        if emsg is None:
            emsg = ""
        else:
            emsg = ". {}".format(emsg)
        super().__init__(
            "Config option value <{}>(type:{}) for <{}> option did not pass the validation check: [{}]{}".format(
                    option, type(option), name, validator, emsg))