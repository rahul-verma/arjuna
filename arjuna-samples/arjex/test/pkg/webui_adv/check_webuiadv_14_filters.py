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

from arjuna import *

@test
def check_filters_coded_index(request, wordpress):
    pass_label = wordpress.element(tags="input", pos=2)
    print(pass_label.source.content.all)
    pass_label = wordpress.element(tags="input", pos="first")
    print(pass_label.source.content.all)
    pass_label = wordpress.element(tags="input", pos="last")
    print(pass_label.source.content.all)
    pass_label = wordpress.element(tags="input", pos="random")
    print(pass_label.source.content.all)
