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

import threading

from arjuna.core import *


def get_current_thread_name():
    return threading.current_thread().name


def create_thread(thread_name, runnable):
    ArjunaCore.register_thread(get_current_thread_name(), thread_name)
    return threading.Thread(runnable, thread_name)


def create_base_thread(thread_name, runnable):
    ArjunaCore.register_new_thread(thread_name)
    return threading.Thread(runnable, thread_name)
