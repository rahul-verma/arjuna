import unittest
from arjuna.tpi import Arjuna

class BaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex-new")
        self.__automator = None
        self.__config = None

    @property
    def automator(self):
        return self.__automator

    @property
    def config(self):
        return self.__config

    def setUp(self):
        self.__automator = Arjuna.create_gui_automator()
        self.__config = self.automator.config

    def tearDown(self):
        self.automator.quit()

    @property
    def automator(self):
        return self.__automator

    def __launch_automator(config=None, econfig=None):
        # Default Gui automation engine is Selenium
        config = config and config or Arjuna.get_ref_config()
        self.__automator = Arjuna.create_gui_automator(config=config, extended_config=econfig)