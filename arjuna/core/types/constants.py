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

from arjuna.tpi.constant import *
from arjuna.core.constant import *

TRUES = {"on", "ON", "true", "TRUE", "yes", "YES"}
FALSES = {"off", "OFF", "false", "FALSE", "no", "NO"}

NA_STRING = "NA"
NOTSET_STRING = "-"
NONE_STRING = "NONE"
NONE_EQUIV_STRINGS = {NA_STRING, NA_STRING.lower(), NOTSET_STRING, NOTSET_STRING.lower(), NONE_STRING, NONE_STRING.lower()}

NUMBER_TYPES = {ValueType.NUMBER, ValueType.INTEGER, ValueType.DOUBLE}

EMPTY_SEQ = ()
