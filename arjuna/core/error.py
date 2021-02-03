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

##########################################################
# Raised and consumed by internal implementation of Arjuna
##########################################################

from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData

class ArjunaException(Exception):
    def __init__(self, message, scrreenshots_path=None, child=None):
        # child is child exception
        super().__init__(message)

        self.screenshot_path = scrreenshots_path
        self.child_Exceptions = []
        if child:
            try:
                raise child
            except ArjunaException as e:
                self.__extract_child_Exceptions(e);
                # } catch (java.lang.reflect.Invocation_target_exception f) {
                #     if (ArjunaException.class.is_assignable_from(f.get_target_exception().get_class())) {
                #         ArjunaException z = (ArjunaException) f.get_target_exception();
                #         extract_child_Exceptions(z);
                #     } else {
                #         insert_child_Exception(f);
                #     }
            except Exception as f:
                self.__insert_child_Exception(f);

    def contains_screenshot(self):
        return self.screenshot_path is not None

    def get_screenshot_path(self):
        return self.screenshot_path

    def set_screenshot_path(self, path):
        self.screenshot_path = path

    def __insert_child_Exception(self, e):
        self.child_Exceptions.append(e)

    def __extract_child_Exceptions(self, e):
        child_Exceptions = e.get_child_Exceptions()
        self.child_Exceptions.extend(child_Exceptions)

    def get_child_Exceptions(self):
        return self.child_Exceptions


def message_formatter(text, component=None, object_name=None, method_name=None, code=None):
    m = ""
    m = m + component and "{}::".format(component) or ""
    m = m + object_name and "{}::".format(object_name) or ""
    m = m + method_name and "{}::".format(method_name) or ""
    m = m + code and "{}::".format(code) or ""
    m = m + text
    return m


class Problem(ArjunaException):
    def __init__(self, text, screenshot_path, exc, component=None, object_name=None, method_name=None, code=None):
        super().__init__(message_formatter(text, component, object_name, method_name, code), exc, screenshot_path);
        self.problem_component = component;
        self.problem_object = object_name;
        self.problem_method = method_name;
        self.problem_code = code;

    def get_problem_component(self):
        return self.problem_component

    def get_problem_object(self):
        return self.problem_object

    def get_problem_method(self):
        return self.problem_method

    def get_problem_code(self):
        return self.problem_code

    def get_problem_text(self):
        return self.get_message()


class DirReaderFinishedException(Exception):
    def __init__(self):
        super().__init__("No more files.")


class UnsupportedRepresentationException(Exception):
    def __init__(self, klass_user_friendly_name, method, str_source_value, target_value_type):
        super().__init__(
            "Value.{}(): Can not represent {} types containing >>{}<< as {}.".format(method, str_source_value,
                                                                                     klass_user_friendly_name,
                                                                                     target_value_type))


class IncompatibleInputForValueException(Exception):
    def __init__(self, value, actual, value_type):
        super().__init__(
            "Incompatible input types >>{}<< (type: {}) supplied for creating {}.".format(value, actual, value_type))


class StringKeyValueContainerLookupException(Exception):
    def __init__(self,key):
        super().__init__("Invalid Key [{}] used for string key types container lookup.".format(key))

class WaitableError(Exception):

    def __init__(self, message):
        super().__init__(message)

def format_msg(msg):
    return msg and  "Error message: {}".format(msg) or ""

class _WidgetNotFoundError(WaitableError):

    def __init__(self, elem_name, *locators, container=None, relations=None, filters=None, message=None):
        container = container and  " in {}".format(container) or ""
        relations = relations and  " with relations {}".format(relations) or ""
        filters = filters and  " and filters {}".format(filters) or ""
        message = format_msg(message)
        super().__init__("{} not found using any of the locators: {}{}{}{}.{}".format(elem_name, GuiWidgetMetaData.locators_as_str(locators), relations, filters, container, message))

class _WidgetPresentError(WaitableError):

    def __init__(self, elem_type, *locators, message=None):
        message = message = format_msg(message)
        super().__init__("{} expected to be absent but still present for one of the locators: {}.{}".format(elem_type, GuiWidgetMetaData.locators_as_str(locators), message))

class GuiWidgetNotFoundError(_WidgetNotFoundError):

    def __init__(self, *locators, container=None, relations=None, filters=None, message=None):
        super().__init__("GuiWidget", *locators, container=container, relations=relations, filters=filters, message=message)

class _GuiWidgetPresentError(_WidgetPresentError):

    def __init__(self, *locators, message=None):
        super().__init__("GuiWidget", *locators, message=message)

class GuiWidgetNotReadyError(WaitableError):

    def __init__(self, message):
        super().__init__("GuiWidget is NOT ready for interaction. Tool message: {}".format(message))

class GuiWidgetTextNotSetError(WaitableError):

    def __init__(self, message):
        super().__init__(". Tool message: {}".format(message))

class ChildWindowNotFoundError(_WidgetNotFoundError):

    def __init__(self, *locators):
        super().__init__("Child window", *locators)

class ChildFrameNotFoundError(_WidgetNotFoundError):

    def __init__(self, *locators):
        super().__init__("Frame", *locators)

class ArjunaTimeoutError(WaitableError):

    def __init__(self, context, message):
        super().__init__(". Timeout in {}. Error Message: {}".format(context, message))  

class DataSourceFinished(StopIteration):
    def __init__(self, msg=None):
        super().__init__(msg is None and "Done" or msg)


class YamlError(Exception):
    '''
        Raised when there is an eror in Yaml structure or there is an error in its expected format in the context where it is used in Arjuna.
    '''

    def __init__(self, msg):
        super().__init__(msg)

class YamlUndefinedSectionError(Exception):
    '''
        Raised when the YamlList does not have the provided section key.
    '''

    def __init__(self, msg):
        super().__init__(msg)

class YamlListIndexError(Exception):
    '''
        Raised when the YamlList does not have the provided index.
    '''

    def __init__(self, msg):
        super().__init__(msg)

class TestGroupsFinished(Exception):
    pass

class ExclusionRuleMet(Exception):
    
    def __init__(self, rule):
        super().__init__("An exclusion rule was met for the object.")
        self.__rule = rule

    @property
    def rule(self):
        return self.__rule

class NoInclusionRuleMet(Exception):
    
    def __init__(self):
        super().__init__("None of the include rules were met.")


class InvalidSelectionRule(Exception):
    pass


class RulePatternDoesNotMatchError(Exception):

    def __init__(self, rule_str, pattern_class, expected_format):
        super().__init__(f"{rule_str} is not a {pattern_class.__name__}. Expected format: {expected_format}")
