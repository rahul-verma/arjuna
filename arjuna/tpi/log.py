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

from arjuna.tpi.helpers.audit import Stack

def __log(invoker, level, msg, *args, contexts=None, **kwargs):
    from arjuna import Arjuna
    if type(contexts) is str:
        contexts = (contexts,)
    elif contexts is None:
        contexts = ("default",)
    contexts = set(contexts)
    getattr(Arjuna.get_logger(), level)(msg, *args, extra={'invoker': invoker, 'contexts':contexts, 'config':Arjuna.get_config()}, **kwargs)

def log_trace(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "trace", msg, *args, contexts=contexts, **kwargs)

def log_debug(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "debug", msg, *args, contexts=contexts, **kwargs)

def log_info(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "info", msg, *args, contexts=contexts, **kwargs)

def log_warning(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "warning", msg, *args, contexts=contexts, **kwargs)

def log_error(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "error", msg, *args, contexts=contexts, **kwargs)

def log_fatal(msg, *args, contexts=None, **kwargs):
    __log(Stack.get_invoker(), "fatal", msg, *args, contexts=contexts, **kwargs)