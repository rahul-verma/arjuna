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

import os
import tempfile
import json

from arjuna.tpi.constant import ArjunaOption
from arjuna.core.har import Har
from arjuna.tpi.protocol.network_recorder import NetworkRecorder
from arjuna.tpi.tracker import track

@track("trace")
class BrowserMobNetworkRecorder(NetworkRecorder):

    def __init__(self, automator):
        super().__init__()
        self.__automator = automator
        self.__start()

    @property
    def _proxy(self):
        return self.__automator.dispatcher.proxy

    def __new_har(self):
        # from arjuna.tpi.data.generator import Random
        # temp_dir = self.__automator.config.value(ArjunaOption.TEMP_DIR)
        # har_file_path = os.path.join(temp_dir, "{}.har".format(Random.ustr()))
        self._proxy.new_har(options={"captureHeaders":True,"captureCookies":True,"captureContent":True})

    def _is_active(self):
        return self._proxy is not None

    def __start(self):
        if self._proxy is None: return
        self.__new_har()
        self._proxy.new_page(title="Ignore")

    def _record(self, title):
        self.__new_har()
        self._proxy.new_page(title=title)

    @property
    def har(self):
        if not self._is_active(): return None
        return self._proxy.har

    def _register(self):
        from arjuna import Arjuna, ArjunaOption
        har = Har.from_har(self.har)
        filter_resources = self.__automator.config.value(ArjunaOption.REPORT_NETWORK_FILTER)
        for packet in har.get_pagewise_network_packet_info(filter_resources=filter_resources):
            Arjuna.get_report_metadata().add_network_packet_info(packet)
        self.__new_har() # This is done to clear har.
        self._proxy.new_page(title="Ignore")

