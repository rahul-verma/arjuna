from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *


@test_function
def test(my):

    automator = Arjuna.create_gui_automator()

    automator.Browser().go_to_url("https://www.google.com")
    print(automator.MainWindow().get_title())
    automator.quit()

