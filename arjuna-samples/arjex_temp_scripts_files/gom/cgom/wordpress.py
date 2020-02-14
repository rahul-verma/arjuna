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

from arjuna import *
from .home import HomePage

class WordPress(WebApp):

    def __init__(self, gns_format="sgns"):
        self.__gns_format = gns_format
        Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex")
        config = Arjuna.get_ref_config()
        super().__init__(config=config, base_url=config.get_user_option_value("wp.login.url").as_str(), gns_dir="{}_wordpress".format(gns_format.lower()))

    @property
    def gns_format(self):
        return self.__gns_format

    def launch(self):
        super().launch()
        return HomePage(self)