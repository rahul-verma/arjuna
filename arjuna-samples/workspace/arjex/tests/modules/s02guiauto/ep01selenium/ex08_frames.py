from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *
from arjuna.tpi.guiauto import With

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)

    automator.element(With.link_text("Posts")).click()
    automator.element(With.link_text("Add New")).click()

    automator.element(With.id("title")).set_text("Sample")

    tinymce = With.id("tinymce")
    publish = With.id("publish")

    # Frame by identifier and jump to root
    automator.Frame(With.id("content_ifr")).focus()
    automator.element(tinymce).set_text("This is a test - frame by name.")
    automator.DomRoot().focus()
    automator.element(publish).click()

    # Frame by index
    automator.Frame(With.index(0)).focus()
    automator.element(tinymce).set_text("This is a test - frame by index.")
    automator.DomRoot().focus()
    automator.element(publish).click()

    # jump to parent frame
    frame = automator.Frame(With.xpath("//iframe"))
    frame.focus()
    automator.element(tinymce).set_text("This is a test - jumping to parent after this.")
    frame.ParentFrame().focus()
    automator.element(publish).click()
    
    WPLoginLogout.logout(automator)
