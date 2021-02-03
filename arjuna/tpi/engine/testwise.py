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

class CurrentTestWiseContainer:

    def __init__(self):
        self.__images = {}
        self.__network_packets = {}
        self.__test_node_id = None

    @property
    def current_test_node_id(self):
        return self.__test_node_id

    @current_test_node_id.setter
    def current_test_node_id(self, node_id):
        self.__test_node_id = node_id

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
        html = '<div class="requets"><h3>&nbsp;&nbsp;Network Packets</h3>'
        import html as py_html
        if self.network_packets:
            for np in self.network_packets:
                req_str = py_html.escape(str(np.request))
                res_str = py_html.escape(str(np.response))
                label = np.label
                if np.sub_network_packets:
                    expander = '<span class="expand">+</span>'
                else:
                    expander = ''
                if req_str != "":
                    html += f'<div class="reqcontent"><p><table class="noborder"><tr><td>{expander}</td><td><button data-request="{req_str}" data-response="{res_str}" onclick="openModal(event)">{label}</button></td></tr></p>'
                else:
                    html += f'<div class="reqcontent"><p><table class="noborder"><tr><td>{expander}</td><td>{label}</td></tr></p>'
                for redir in np.sub_network_packets:
                    req_str = py_html.escape(str(redir.request))
                    res_str = py_html.escape(str(redir.response))
                    label = redir.label
                    html += f'<div class="reqcontent"><p><tr class="redir"><td></td><td><button class="redir_button" data-request="{req_str}" data-response="{res_str}" onclick="openModal(event)">{label}</button></td></tr></p></div>'
                html += '</table></div>' # np
        html += '</div>' # headline
        html += '</div>' # id="image"
        return html

    def has_content(self):
        if self.images or self.network_packets:
            return True
        else:
            return False

    def as_report_html(self, *, include_images=True, include_network=True):
        if (not include_images) and (not include_network):
            return None
        html = '<div class="image">'
        if include_images:
            html += self._get_images_html()
        if include_network:
            html += self._get_packets_html()
        html += "</div>"
        return html

    def add_image(self, image):
        tname = threading.current_thread
        if tname not in self.__images:
            self.__images[tname] = []
        self.__images[tname].append(image)

    def add_network_packet_info(self, packet):
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

