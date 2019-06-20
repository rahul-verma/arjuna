from arjuna.setu.webclient.requester import SetuAgentRequester


class SetuActorRequester():

    def __init__(self, base_url):
        super().__init__()
        self.__agent_requester = SetuAgentRequester(base_url)

    def post(self, url_suffix, json_dict):
        return self.__agent_requester.post(url_suffix, json_dict)