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

from arjuna.interact.gui.auto.element.guielement import GuiElement
from arjuna.core.enums import ArjunaOption

class WebAlert:

    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def confirm(self):
        self.automator.dispatcher.confirm_web_alert()
        self.automator.alert_handler.delete_alert()

    def dismiss(self):
        self.automator.dispatcher.dismiss_web_alert()
        self.automator.alert_handler.delete_alert()

    @property
    def text(self):
        return self.automator.dispatcher.get_text_from_web_alert()

    @text.setter
    def text(self, text):
        self.automator.dispatcher.send_text_to_web_alert(text)