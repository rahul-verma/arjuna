from arjuna.tpi import Arjuna
from arjuna.interact.gui.gom import WebApp
from .home import HomePage

class WordPress(WebApp):

    def __init__(self, gns_format="sgns"):
        self.__gns_format = gns_format
        Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex")
        config = Arjuna.get_ref_config()
        super().__init__(config=config, base_url=config.get_user_option_value("wp.login.url").as_str(), ns_dir="{}_wordpress".format(gns_format.lower()))

    @property
    def gns_format(self):
        return self.__gns_format

    def launch(self):
        super().launch()
        return HomePage(self, self._automator)