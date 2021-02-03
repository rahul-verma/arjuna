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

from arjuna.tpi.constant import ArjunaOption

class WebAlert:

    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def confirm(self):
        self.__automator.dispatcher.confirm_web_alert()
        self.__automator.alert_handler.delete_alert()

    def dismiss(self):
        self.__automator.dispatcher.dismiss_web_alert()
        self.__automator.alert_handler.delete_alert()

    @property
    def text(self):
        return self.__automator.dispatcher.get_text_from_web_alert()

    @text.setter
    def text(self, text):
        self.__automator.dispatcher.send_text_to_web_alert(text)