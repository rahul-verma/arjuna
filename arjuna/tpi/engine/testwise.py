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

import threading
from collections import namedtuple

NetworkPacket = namedtuple("NetworkPacket", "request response")

SAMPLE_HTML = '''
<p><p>
<!-- Trigger/Open The Modal -->
<button id="b1" onclick="openModal(event)">Open Modal</button>

<!-- The Modal -->
<div id="b1-modal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span id="b1-span" class="close">&times;</span>
    <p>Some text in the Modal..</p>
  </div>

</div>

<!-- Trigger/Open The Modal -->
<button id="b2" onclick="openModal(event)">Open Modal</button>

<!-- The Modal -->
<div id="b2-modal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span id="b2-span" class="close">&times;</span>
    <p>Some text b2b2b222b in the Modal..</p>
  </div>

</div>
'''

class CurrentTestWiseContainer:

    def __init__(self):
        self.__images = {}
        self.__network_packets = {}

    @property
    def images(self):
        try:
            return tuple(self.__images[threading.current_thread])
        except KeyError:
            return tuple()

    @property
    def network_packets(self):
        try:
            return tuple(self.__network_packets[threading.current_thread])
        except KeyError:
            return tuple()

    def _get_images_html(self):
        if not self.images: return ""
        html = "<p><p><h3>&nbsp;&nbsp;Screenshots and Images</h3><p>"
        if self.images:
            for image in self.images:
                fpath = "../screenshot/{}".format(image.file_name)
                #img_elem = '''<img src="data:image/png;base64,{}"/>'''.format(image.base64)
                #html += '<a href="{}" onclick="openModalImage(event)">{}</a>'.format(fpath, img_elem)

                html += '''<img class="screenshot" onclick="openModalImage(event)" href="{}" src="data:image/png;base64,{}"/>'''.format(fpath, image.base64)
        html += "<p><p>"
        return html

    def _get_packets_html(self):
        if not self.network_packets: return ""
        html = "<p><p><h3>&nbsp;&nbsp;Network Packets</h3><p>"
        if self.network_packets:
            for np in self.network_packets:
                html += '<button data-request="{}" data-response="{}" onclick="openModal(event)">Open Modal</button>'.format(str(np.request), str(np.response))
        html += "<p><p>"
        return html

    def has_content(self):
        return self.images or self.network_packets

    def as_report_html(self):
        html = '<div class="image">'
        html += self._get_images_html()
        html += self._get_packets_html()
        html += "</div>"
        return html

    def add_image(self, image):
        tname = threading.current_thread
        if tname not in self.__images:
            self.__images[tname] = []
        self.__images[tname].append(image)

    def add_network_packet(self, packet):
        tname = threading.current_thread
        if tname not in self.__network_packets:
            self.__network_packets[tname] = []
        self.__network_packets[tname].append(packet)

    def clear(self):
        tname = threading.current_thread
        if tname in self.__images:
            del self.__images[tname]
        if tname in self.__network_packets:
            del self.__network_packets[tname]

