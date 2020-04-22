# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from arjuna.core.exceptions import *

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
        Raised when a GuiWidget is unexpectedly found using a GuiWidgetLocator object. Involves Dynamic Waiting for absence.
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
        Raised when a GuiWidget is NOT found using a GuiWidgetLocator object. Involves Dynamic Waiting for presence.
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
