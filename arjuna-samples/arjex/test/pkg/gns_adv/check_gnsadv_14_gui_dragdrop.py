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

@test
def check_gns_drag_drop(request):
    app = GuiApp(gns_dir="common", label="common", url="https://jqueryui.com/droppable/")
    app.launch()
    frame = app.gns.jframe
    frame.switch_to_me()
    drag = app.gns.todrag
    drop = app.gns.todrop
    drag.drop(drop)
    app.switch_to_dom_root()
    app.quit()


@test
def check_gns_attr(request):
    app = GuiApp(gns_dir="common", label="common", url="https://jqueryui.com/droppable/")
    app.launch()
    app.element(attr=attr(style="display"))
    app.quit()
