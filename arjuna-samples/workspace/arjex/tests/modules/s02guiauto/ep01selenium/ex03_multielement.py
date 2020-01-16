from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *
from arjuna.tpi.guiauto import With

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator);

    automator.element(With.link_text("Posts")).click()
    automator.element(With.link_text("Categories")).click()

    checkboxes = automator.multi_element(With.name("delete_tags[]"))
    checkboxes.IndexedElement(0).uncheck()
    checkboxes.IndexedElement(0).check()
    checkboxes.IndexedElement(0).check()
    checkboxes.IndexedElement(1).check()

    WPLoginLogout.logout(automator)
