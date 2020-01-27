from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = login()

wordpress.ui.execute_javascript("document.getElementsByClassName('welcome-view-site')[0].click();")
wordpress.ui.element(With.link_text("Site Admin")).wait_until_clickable()

logout(wordpress)