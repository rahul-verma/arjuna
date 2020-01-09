from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

login(automator)

automator.Element(With.link_text("Posts")).click()
automator.Element(With.link_text("Add New")).click()

With tinymce = With.id("tinymce")
With publish = With.id("publish")

# Frame by identifier and jump to root
automator.Frame(With.id("content_ifr")).focus()
automator.Element(tinymce).set_text("This is a test - frame by name.")
automator.dom_root().focus()
automator.Element(publish).click()

# Frame by index
automator.Frame(With.index(0)).focus()
automator.Element(tinymce).set_text("This is a test - frame by index.")
# Focusing on root from frame itself
automator.dom_root.focus()
automator.Element(publish).click()

# jump to parent
Frame frame = automator.Frame(With.xpath("//iframe"))
frame.focus()
automator.Element(tinymce).set_text("This is a test - jumping to parent after this.")
frame.parent.focus()
automator.Element(publish).click()

logout(automator)