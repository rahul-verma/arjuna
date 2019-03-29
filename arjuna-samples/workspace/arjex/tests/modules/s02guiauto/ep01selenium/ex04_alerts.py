from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)

    automator.execute_javascript("alert('dummy')")
    automator.Alert().confirm()
    automator.execute_javascript("alert('dummy')")
    automator.Alert().dismiss()

    automator.execute_javascript("alert('Sample')")
    alert = automator.Alert()
    text = alert.get_text()
    assert alert.get_text() == "Sample"
    alert.confirm()

    automator.execute_javascript("prompt('Are You Sure?')")
    alert = automator.Alert()
    alert.send_text("Yes")
    alert.confirm()

    WPLoginLogout.logout(automator)
