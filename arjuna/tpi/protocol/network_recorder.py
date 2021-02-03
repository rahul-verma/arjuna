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

import abc
from arjuna.tpi.helper.image import Image
from arjuna.tpi.tracker import track


@track("trace")
class NetworkRecorder(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__in_recording_mode = False

    def is_recording(self):
        return self.__in_recording_mode

    @abc.abstractmethod
    def _is_active(self):
        pass

    def record(self, title):
        '''
            Start recording.

            Arguments:
                title: Title representing all captured traffic.
        '''
        if not self._is_active(): return
        if self.is_recording():
            self.register()
        self._record(title=title)
        self.__in_recording_mode = True

    @abc.abstractmethod
    def _record(self, title):
        pass

    def register(self):
        '''
            Register the current recorded traffic with Arjuna.
        '''
        if not self._is_active(): return
        if not self.is_recording(): return
        self._register()
        self.__in_recording_mode = False

    @abc.abstractmethod
    def _register(self):
        pass