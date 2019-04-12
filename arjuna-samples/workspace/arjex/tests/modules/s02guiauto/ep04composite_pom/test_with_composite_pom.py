from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *

from .app_pages import HomePage


@test_function
def test(my):

    automator = Arjuna.create_gui_automator()

    home = HomePage(automator)
    home\
    .login()\
    .left_nav\
    .go_to_settings()\
    .tweak_settings()\
    .top_nav\
    .logout()

    automator.quit()
