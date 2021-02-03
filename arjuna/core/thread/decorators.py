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

import functools
import threading
import types

from arjuna.core.adv.wrappers import ClassPassThrough


# From blog post by Daniel Holden at http://theorangeduck.com/page/synchronized-python
def sync_function(func):
    # reentrant lock to supprt recursion
    func.__lock__ = threading.RLock()

    @functools.wraps(func)
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def sync_class(klass):
    for key in klass.__dict__:
        val = klass.__dict__[key]
        if type(val) is types.FunctionType:
            decorator = sync_function
            setattr(klass, key, decorator(val))

    return klass


# From blog post by Daniel Holden at http://theorangeduck.com/page/synchronized-python
# To use the following you should create self.lock = threading.RLock() in __init__
# Per instance basis lock
def sync_method(lock_name):
    def decorator(method):
        @functools.wraps(method)
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator
