from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

automator.element(With.link_text("Posts")).click()
automator.element(With.link_text("Add New")).click()

tinymce = With.id("tinymce")
publish = With.id("publish")

# Frame by identifier and jump to root
automator.frame(With.id("content_ifr")).focus()
automator.element(tinymce).set_text("This is a test - frame by name.")
automator.dom_root.focus()
automator.element(publish).click()

# Frame by index
automator.frame(With.index(0)).focus()
automator.element(tinymce).set_text("This is a test - frame by index.")
# Focusing on root from frame itself
automator.dom_root.focus()
automator.element(publish).click()

# jump to parent
frame = automator.frame(With.xpath("//iframe"))
print(frame)
frame.focus()
automator.element(tinymce).set_text("This is a test - jumping to parent after this.")
frame.parent.focus()
automator.element(publish).click()

logout(automator)