from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = login()

wordpress.ui.element(With.link_text("Posts")).click()
wordpress.ui.element(With.link_text("Categories")).click()

check_boxes = wordpress.ui.multi_element(With.name("delete_tags[]"))
check_boxes[0].uncheck()
check_boxes[0].check()
check_boxes[0].check()
check_boxes[0].uncheck()

check_boxes.first_element.uncheck()
print(check_boxes.first_element.source.content.all)
check_boxes.last_element.uncheck()
check_boxes.random_element.uncheck()

logout(wordpress)