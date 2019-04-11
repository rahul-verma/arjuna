import inspect
from arjuna.tpi.enums import ArjunaOption
from .driverelement import SeleniumDriverElement


class SeleniumDriver:

    def __init__(self, setu_id, requester):
        self.__setu_id = setu_id
        self.__requester = requester

    def create_gui_element_dispatcher(self, element_setu_id):
        return SeleniumDriverElement()
        self.__dispatcher.create_gui_element_dispatcher(element_setu_id)

    def __post_to_actor(self, action, actor_uri, **kwargs):
        input_dict = {"automatorSetuId" : self.setu_id}
        input_dict.update(kwargs)
        json_dict = {
            "action" : action,
            "args" : input_dict
        }
        return self.__requester.post(actor_uri, json_dict)

    def post_action(self, **kwargs):
        action = inspect.stack()[1].function
        return self.__post_to_actor(action, "/automator/action", **kwargs)

    def post_other(self, url, **kwargs):
        action = inspect.stack()[1].function
        return self.__post_to_actor(action, url, **kwargs)

    @property
    def setu_id(self):
        return self.__setu_id

    def launch(self, config):
        self.post_other("/automator/launch", 
        automatorName=config["arjunaOptions"][ArjunaOption.GUIAUTO_AUTOMATOR_NAME.name], 
        config=config)

    def quit(self):
        self.post_action()

    def go_to_url(self, url):
        self.post_action(url=url)

    def go_back_in_browser(self):
        self.post_action()

    def go_forward_in_browser(self):
        self.post_action()

    def refersh_browser(self):
        self.post_action()

    def execute_javascript(self, script):
        self.post_action(script=script)

    def take_screenshot(self):
        self.post_action()

    def find_element(self, child_gui_element_set_id, with_type, with_value):
        self.post_action(
            elementSetuId = child_gui_element_set_id,
            withType = with_type,
            withValue = with_value
        )

    def find_multielement(self, child_gui_element_set_id, with_type, with_value):
        response = self.post_action(
            elementSetuId = child_gui_element_set_id,
            withType = with_type,
            withValue = with_value
        )

        return response["data"]["instanceCount"]

    def __get_value_from_response(self, response, key):
        if "data" not in response:
            raise Exception("Setu actor json response: {} does not contain 'data' key.")
        elif key not in response:
            raise Exception("Setu actor json response: {} does not contain key <{}> in data section.")
        else:
            return response["data"][key]

    def __get_result(self, response):
        return self.__get_value_from_response(response, "result")

    def get_current_window_handle(self):
        response = self.post_action()
        return self.__get_result(response)

    def get_current_window_title(self):
        response = self.post_action()
        return self.__get_result(response)

    def maximize_current_window(self):
        self.post_action()

    def get_current_window_size(self):
        response = self.post_action()
        size = self.__get_result(response)
        return size["width"], size["height"]

    def get_all_window_handles(self):
        response = self.post_action()
        return self.__get_result(response)

    def focus_on_window(self, handle):
        self.post_action(handle=handle)

    def close_current_window(self):
        self.post_action()

    def is_web_alert_present(self):
        response = self.post_action()
        return self.__get_result(response)

    def confirm_web_alert(self):
        self.post_action()

    def dismiss_web_alert(self):
        self.post_action()

    def get_text_from_web_alert(self):
        response = self.post_action()
        return self.__get_result(response)

    def send_text_to_web_alert(self,text):
        self.post_action(text=text)

    def get_current_mobile_view_context(self):
        response = self.post_action()
        return self.__get_result(response)

    def get_all_mobile_view_contexts(self):
        response = self.post_action()
        return self.__get_result(response)

    def focus_on_mobile_view_context(self, view_context):
        self.post_action(viewContext=view_context)

    def focus_on_frame(self, elem_setu_id, is_instance_action=False, instance_index=0):
        if is_instance_action:
            self.post_action(elementSetuId=elem_setu_id, isInstanceAction=is_instance_action, instanceIndex=instance_index)
        else:
            self.post_action(elementSetuId=elem_setu_id)

    def focus_on_parent_frame(self):
        self.post_action()

    def focus_on_dom_root(self):
        self.post_action()
