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

@test
def check_user_options(request):
    '''
        For this test:
        You must add target.url = "https://google.com" to userOptions in project.conf to see the impact.
    '''
    # Just like Arjuna options, C works for user options in reference config
    url = C("target.url")

    cb = request.config.builder
    cb.option("target.title", "Google")
    # or
    cb["target.title"] = "Google"
    # or
    cb.target_title = "Google"
    config = cb.register()

    title = config.target_title
    #or
    title = config["target.title"] # or config.value("target.title") or other variants seen earlier
    url = config.value("target.url") # Ref user options are available in new config as well.

    google = WebApp(base_url=url, config=config)
    google.launch()
    request.asserter.assert_equal(title, google.title, "Page title does not match.")
    google.quit()