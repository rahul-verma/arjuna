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

import os
import tempfile
import json

from arjuna.tpi.constant import ArjunaOption
from arjuna.core.har import Har
from arjuna.tpi.protocol.network_recorder import NetworkRecorder

class BrowserMobNetworkRecorder(NetworkRecorder):

    def __init__(self, automator):
        super().__init__()
        self.__automator = automator
        self.__current_title = None
        self.__current_har_file_path = None
        self.__started = False

    @property
    def _proxy(self):
        return self.__automator.dispatcher.proxy

    def __new_har(self):
        from arjuna.tpi.data.generator import Random
        temp_dir = self.__automator.config.value(ArjunaOption.TEMP_DIR)
        har_file_path = os.path.join(temp_dir, "{}.har".format(Random.ustr()))
        self._proxy.new_har(options={"captureHeaders":True,"captureCookies":True,"captureContent":True})

    def _start(self, *, title):
        if self._proxy is None: return
        if self.active and title.lower() == self.current_title.lower():
            return
        if self.active:
            self.stop()
        self.__new_har()
        self.__started = True
        self.current_title = title

    @property
    def active(self):
        return self.__started

    @property
    def current_title(self):
        if not self.active:
            raise Exception("The recorder is not active. You can not get page name for a stopped recorder.")
        return self.__current_title

    @current_title.setter
    def current_title(self, title):
        if self._proxy is None: return
        if not self.active:
            raise Exception("The recorder is not active. You can not set page name for a stopped recorder.")
        self._proxy.new_page(title=title)
        self.__current_title = title

    @property
    def har(self):
        if self._proxy is None: return None
        return self._proxy.har

    def _stop(self):
        if self._proxy is None: return
        if not self.active:
            raise Exception("The recorder is not active. You can not stop an already stopped recorder.")
        from arjuna import Arjuna, ArjunaOption
        har = Har.from_har(self.har)
        filter_resources = self.__automator.config.value(ArjunaOption.REPORT_NETWORK_FILTER)
        for packet in har.get_pagewise_network_packet_info(filter_resources=filter_resources):
            Arjuna.get_report_metadata().add_network_packet_info(packet)
        self.__new_har() # This is done to clear har.

