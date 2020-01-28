from commons import *
from arjuna import *

init_arjuna()
wordpress = login()

wordpress.ui.element(With.link_text("Settings")).click()

date_format = wordpress.ui.radio_group(With.name("date_format"))
print(date_format.has_value_selected("Y-m-d"))
print(date_format.has_index_selected(1))
print(date_format.value)
date_format.select_value(r"\c\u\s\t\o\m")
date_format.select_index(2)

logout(wordpress)