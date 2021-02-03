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

from commons import *
from arjuna import *

init_arjuna()

wordpress = None
element = None

def setup():
    global wordpress
    wordpress = create_wordpress_app()

def cleanup():
    global wordpress
    global element
    print(element.source.content.root)
    wordpress.quit()
    element = None
    wordpress = None

setup()
element = wordpress.ui.element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
element = wordpress.ui.element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return null"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return undefined"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return []"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return 1"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return [1,2]"))
# cleanup()
