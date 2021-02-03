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

from arjuna import *

'''
Code is kept redundant across methods for the purpose of easier learning.
'''

@test
def check_project_conf(request):
    '''
        For this test:
        You must add browser.name = firefox to arjuna_options in project.yaml to see the impact.
        It changes the default browser from Chrome to Firefox across the project.
    '''
    google = GuiApp(url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.title, "GuiPage title does not match.")
    google.quit()