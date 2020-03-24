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

# Automator vs DomRoot vs Frame sources
automator.element(With.link_text("Posts")).click()
automator.element(With.link_text("Add New")).click()
print_source_info(automator.source)

print_source_info(automator.dom_root.source)

# Frame source

frame = automator.frame(With.id("content_ifr"))
frame.focus()
print_source_info(frame.source)

# custom drop down
url = automator.config.user_options.value("narada.ex.dropdown.url")
automator.browser.go_to_url(url)

conf = GuiInteractionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = automator.dropdown(
    With.id("DropDown"),
    option_container_locators=With.class_name("dropdown"),
    option_locators=With.class_name("dropdown-item")
)
    
dropdown.configure(conf)
print_source_info(dropdown.source)

logout(automator)