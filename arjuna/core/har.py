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

import json
from haralyzer import HarParser, HarPage
from arjuna.tpi.httpauto.request import HttpRequest
from arjuna.tpi.httpauto.request import HttpResponse

from arjuna.tpi.helper.arjtype import NetworkPacketInfo

class Har:

    def __init__(self, pydict):
        self.__har = pydict
        self.__har_parser = HarParser(pydict)

    def get_pagewise_network_packet_info(self, filter_resources=True):
        page_network_info = []
        from arjuna import Arjuna, ArjunaOption
        for har_page in self.__har_parser.pages:
            sub_network_packets = []
            if filter_resources:
                entries = har_page.filter_entries(content_type=".*(text/plain|application/xhtml+xml|text/html|json|application/xml|text/xml)")
            else:
                entries = har_page.entries
            for entry in entries:
                req_method = entry['request']['method']
                req_url = entry['request']['url']
                req_headers= {header['name']: header['value'] for header in entry['request']['headers']}
                if 'content' in entry['request']:
                    req_content = entry['request']['content']['text']
                else:
                    req_content = None

                req_repr = HttpRequest.repr_as_str(
                    method=req_method,
                    url=req_url,
                    headers=req_headers,
                    content=req_content
                )

                resp_status = entry['response']['status']
                resp_status_text = entry['response']['statusText']
                resp_headers = {header['name']: header['value'] for header in entry['response']['headers']}
                if 'content' in entry['response']:
                    if 'text' in entry['response']['content']:
                        resp_content = entry['response']['content']['text']
                    else:
                        resp_content = None
                else:
                    resp_content = None

                resp_repr = HttpResponse.repr_as_str(
                    status_code=resp_status,
                    status_msg=resp_status_text,
                    headers=resp_headers,
                    content=resp_content
                )

                sub_network_packets.append(
                    NetworkPacketInfo(
                        label=f"{req_method} {req_url}",
                        request=req_repr,
                        response=resp_repr,
                        sub_network_packets=[]
                    )
                )

            if sub_network_packets:
                page_network_info.append(
                    NetworkPacketInfo(
                        label=har_page.title,
                        request="",
                        response="",
                        sub_network_packets=sub_network_packets
                    )
                )

        return page_network_info

    @classmethod
    def from_har(cls, harobj):
        try:
            return Har(harobj)
        except:
            raise Exception("Invalid HAR object.")

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r") as f:
            return Har(json.loads(f.read()))
