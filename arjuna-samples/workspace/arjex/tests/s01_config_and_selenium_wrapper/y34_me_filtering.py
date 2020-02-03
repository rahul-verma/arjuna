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

from commons import *
from arjuna import *

init_arjuna()
wordpress = login()

wordpress.ui.element(With.link_text("Posts")).click()
wordpress.ui.element(With.link_text("Categories")).click()

cbs = wordpress.ui.multi_element(With.name("delete_tags[]"))
for cb in cbs:
    print(cb.source.content.all)

# wordpress.ui.execute_javascript("arguments[0].style.display = 'none';", cbs[0])
# fcbs = cbs.filter.visible().build()
# for e in fcbs:
#     print(e.source.content.all)

# wordpress.ui.execute_javascript("arguments[0].style.display = 'none';", cbs[1])
# fcbs = cbs.filter.visible().build()
# print("here", fcbs.elements)

print("Let's remove the first checkbox from DOM")
result = wordpress.ui.execute_javascript("try{arguments[0].parentNode.removeChild(arguments[0]); return 1;} catch (err) {return err.message;}", cbs[0])
for cb in cbs:
    try:
        print(cb.get_html())
    except Exception as e:
        # Should get stale element exception
        print(e)

print("Filter stale elements")
fcbs = cbs.filter.active().build()
for cb in fcbs:
    try:
        print(cb.get_html())
    except Exception as e:
        # Should get stale element exception
        print(e)
logout(wordpress)