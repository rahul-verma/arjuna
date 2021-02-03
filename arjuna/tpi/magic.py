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

'''
Arjuna's Magic Functions

The magic functions are single-letter functions which provide easy access to Arjuna's following global containers:
    - Configurations
    - Localizer
    - Contextual Data References.
'''

from arjuna.tpi.engine import Arjuna
from typing import Any
from arjuna.tpi.tracker import track

@track("trace")
def C(query: 'ConfigQuery', *, cname: str=None) -> Any:
    '''
        Get the object for a configuration option.

        Args:
            query: Config query representing a config option in reference or custom configuration.
            cname: (Optional keyword arg) Configuration name. If None Arjuna assumes the reference configuration for this query.

        Returns:
            An object of Any type depending upon the configuration option query.
    '''
    return Arjuna.get_config_value(query, cname=cname)

@track("trace")
def L(query: "L10nQuery", *, locale: 'Locale'=None, bucket: str=None, strict: bool=None) -> str:
    '''
        Get the localized string corresponding to Localization Query.

        Args:
            query: Localization query representing a reference which needs to be localized.
            locale: A Locale enum constant or corresponding string e.g. en
            bucket: A string representing Localization bucket
            strict: If True, exception is raised if query is not resolved, else query is returned. Default is False. 

        Returns:
            A localized string as per the bucket and locale. In non-strict mode, the query itself is returned if localized string is not found.
    '''
    return Arjuna.get_localized_str(query, locale=locale, bucket=bucket, strict=strict)

@track("trace")
def R(query: 'DataRefQuery'="", *, bucket: str=None, context: str=None, index: int=None) -> Any:
    '''
        Get the object for a query from Contextual Data Reference.

        Args:
            query: Data Reference Query representing a reference for which object has to be retrieved.
            bucket: A string representing Data Reference bucket
            context: A string representing Data Reference context
            context: An int representing Data Reference index

        Returns:
            An object of Any type depending upon the Data Reference query.
    '''
    return Arjuna.get_dataref_value(query, bucket=bucket, context=context, index=index)