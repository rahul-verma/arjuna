# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from commons import *
from arjuna import *

init_arjuna()
wordpress = login()

wordpress.ui.element(With.link_text("Posts")).click()
wordpress.ui.element(With.link_text("Add New")).click()

tinymce = With.id("tinymce")
publish = With.id("publish")

# Frame by identifier and jump to root
wordpress.ui.frame(With.id("content_ifr")).focus()
wordpress.ui.element(tinymce).enter_text("This is a test - frame by name.")
wordpress.ui.dom_root.focus()
wordpress.ui.element(publish).click()

# Frame by index
wordpress.ui.frame(With.index(0)).focus()
wordpress.ui.element(tinymce).enter_text("This is a test - frame by index.")
# Focusing on root from frame itself
wordpress.ui.dom_root.focus()
wordpress.ui.element(publish).click()

# jump to parent
frame = wordpress.ui.frame(With.xpath("//iframe"))
print(frame)
frame.focus()
wordpress.ui.element(tinymce).enter_text("This is a test - jumping to parent after this.")
frame.parent.focus()
wordpress.ui.element(publish).click()

logout(wordpress)