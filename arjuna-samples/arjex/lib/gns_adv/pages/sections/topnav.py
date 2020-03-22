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
from enum import Enum, auto
from .base import WPBaseSection

class TopNav(WPBaseSection):

    def logout(self):
        url = C("wp.logout.url")
        self.go_to_url(url)

        self.gns.logout_confirm.click()
        self.gns.logout_msg

        from arjex.lib.gns_adv.pages.home import Home
        return Home(self)