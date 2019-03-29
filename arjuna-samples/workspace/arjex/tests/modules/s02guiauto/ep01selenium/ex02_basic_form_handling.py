from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *

from .wp import WPLoginLogout


@test_function
def test(my):

    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)
    WPLoginLogout.logout(automator)
