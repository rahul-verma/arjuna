'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import requests
import json
import os

from arjuna.setu import Setu


class SetuAgentRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def __convert_response_text_to_json(self, response_text):
        try:
            return json.loads(response_text)
        except:
            raise Exception("Response text is not JSON. Raw response text: " + response_text)

    def __raise_exception_if_error(self, response_dict):
        if response_dict is None:
            raise Exception("Setu Actor's JSON response is null.")
        if (response_dict["result"].lower() == "error"):
            emessage = response_dict.get("emessage", "")
            raise Exception("Agent Error: " + emessage + os.linesep + "Trace: " + response_dict["etrace"])

    def get(self, url):
        req_url = self.base_url + url
        response = requests.get(req_url)
        response_json = json.loads(response.text)
        self.__raise_exception_if_error(response_json)
        return json.loads(response.text, encoding="utf-8")

    def post(self, url, json_dict):
        req_url = self.base_url + url
        response = requests.post(req_url, json=json_dict)
        response_json = self.__convert_response_text_to_json(response.text)
        self.__raise_exception_if_error(response_json)
        return json.loads(response.text)

    def get_base_url(self):
        return self.base_url