from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

automator.execute_javascript("alert('dummy')")
automator.alert.confirm()
automator.execute_javascript("alert('dummy')")
automator.alert.dismiss()

automator.execute_javascript("alert('dummy')")
alert = automator.alert
assert alert.text == "dummy"
alert.confirm()

automator.execute_javascript("prompt('Are You Sure?')")
alert = automator.alert
alert.send_text("Yes")
alert.confirm()

logout(automator)