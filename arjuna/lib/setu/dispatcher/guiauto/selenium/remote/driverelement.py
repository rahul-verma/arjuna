import inspect

class SeleniumDriverElement:

    def __init__(self, automator_setu_id, element_setu_id, requester):
        self.__automator_setu_id = automator_setu_id
        self.__element_set_id = element_setu_id
        self.__requester = requester
        self.__partial = False
        self.__instance_index = 0

    def set_partial(self, index):
        self.__partial = True
        self.__instance_index = index

    @property
    def automator_setu_id(self):
        return self.__automator_setu_id

    @property
    def element_setu_id(self):
        return self.__element_set_id

    @property
    def requester(self):
        return self.__requester

    def post(self, **kwargs):
        input_dict = {
            "automatorSetuId" : self.automator_setu_id,
            "elementSetuId" : self.element_setu_id
        }

        if self.__partial:
            input_dict.update( {
                "isInstanceAction" : True,
                "instanceIndex" : self.__instance_index
            })
        input_dict.update(kwargs)
        json_dict = {
            "action" : inspect.stack()[1].function,
            "args" : input_dict
        }
        return self.__requester.post("/element/action", json_dict)

    def __get_value_from_response(self, response, key, optional=False):
        if "data" not in response:
            if not optional:
                raise Exception("Setu actor json response: {} does not contain 'data' key.".format(response))
            else:
                return None
        elif key not in response["data"]:
            if not optional:
                raise Exception("Setu actor json response: {} does not contain key <{}> in data section.".format(response, key))
            else:
                return None
        else:
            return response["data"][key]

    def __get_result(self, response, optional=False):
        return self.__get_value_from_response(response, "result", optional)

    def find_element(self, child_gui_element_set_id, with_type, with_value):
        self.post(
            childElementSetuId = child_gui_element_set_id,
            withType = with_type,
            withValue = with_value
        )

    def find_multielement(self, child_gui_element_set_id, with_type, with_value):
        response = self.post(
            childElementSetuId = child_gui_element_set_id,
            withType = with_type,
            withValue = with_value
        )

        return response["data"]["instanceCount"]

    def click(self):
        self.post()

    def clear_text(self):
        self.post()

    def send_text(self, text):
        self.post(text=text)

    def is_selected(self):
        response = self.post()
        return self.__get_result(response)

    def is_visible(self):
        response = self.post()
        return self.__get_result(response)

    def is_clickable(self):
        response = self.post()
        return self.__get_result(response)

    def get_tag_name(self):
        response = self.post()
        return self.__get_result(response)

    def get_attr_value(self, attr_name, optional=False):
        response = self.post(attr=attr_name)
        return self.__get_result(response, optional)

    def get_text_content(self):
        response = self.post()
        return self.__get_result(response)