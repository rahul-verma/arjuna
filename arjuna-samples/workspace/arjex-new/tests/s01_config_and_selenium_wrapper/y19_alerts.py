from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

login(automator)

automator.execute_script("alert('dummy')")
automator.alert.confirm()
automator.execute_script("alert('dummy')")
automator.alert.dismiss()

automator.execute_script("alert('dummy')")
alert = automator.alert
assert alert.text == "dummy"
alert.confirm()

automator.execute_script("prompt('Are You Sure?')")
alert = automator.alert
alert.send_text("Yes")
alert.confirm()

logout(automator)