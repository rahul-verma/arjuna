from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = login()

wordpress.ui.execute_javascript("alert('dummy')")
wordpress.ui.alert.confirm()
wordpress.ui.execute_javascript("alert('dummy')")
wordpress.ui.alert.dismiss()

wordpress.ui.execute_javascript("alert('dummy')")
alert = wordpress.ui.alert
assert alert.text == "dummy"
alert.confirm()

wordpress.ui.execute_javascript("prompt('Are You Sure?')")
alert = wordpress.ui.alert
alert.text = "Yes"
alert.confirm()

logout(wordpress)