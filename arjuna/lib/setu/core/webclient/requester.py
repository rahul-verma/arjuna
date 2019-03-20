import requests
import json
import os

class SetuAgentRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def __raise_exception_if_error(self, response_dict):
        if response_dict is None:
            raise Exception("Setu Actor's JSON response is null.")
        if (response_dict["result"].lower() == "error"):
            emessage = response_dict.get("emessage", "")
            raise Exception("Agent Error: " + emessage + os.linesep + "Trace: " + response_dict["etrace"])

    def get(self, url):
        req_url = self.base_url + url
        print("Request URL (GET)::", req_url)
        response = requests.get(req_url)
        response_json = json.loads(response.text)
        self.__raise_exception_if_error(response_json)
        print("Response:: ", os.linesep, response.text)
        return json.loads(response.text)

    def post(self, url, json_dict):
        req_url = self.base_url + url
        print("Request URL (POST)::", req_url)
        print("Request Body (POST)::", os.linesep, json_dict)
        response = requests.post(req_url, json=json_dict)
        print("Response:: ", os.linesep, response.text)
        response_json = json.loads(response.text)
        self.__raise_exception_if_error(response_json)
        return json.loads(response.text)

    def get_base_url(self):
        return self.base_url