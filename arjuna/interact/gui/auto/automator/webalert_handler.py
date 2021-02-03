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

class WebAlertHandler:

    def __init__(self, automator):
        self.__automator = automator
        self.__alert_present = False
        self.__alert = None

    def create_alert(self):
        if self.__alert_present:
            return self.__alert
        else:
            self.wait()
            from arjuna.tpi.guiauto.widget.webalert import WebAlert
            self.__alert_present = True
            alert = WebAlert(self.__automator)
            self.__alert = alert
            return alert

    def delete_alert(self):
        self.__alert_present = False
        self.__alert = None

    def wait(self):
        self.__automator.conditions.AlertIsPresent().wait(max_wait=self.__automator.config.value("guiauto.max.wait"))

    def is_alert_present(self):
        return self.__automator.dispatcher.is_web_alert_present()



