from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

Arjuna.init()
# Default Gui automation engine is Selenium
automator = None
element = None

def setup():
    global automator
    automator = Arjuna.create_gui_automator(Arjuna.get_central_config())
    go_to_wp_home(automator)

def cleanup():
    print(element.source.content.root)
    global automator
    global element
    automator.quit()
    element = None
    automator = None

setup()
element = automator.Element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
element = automator.Element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

setup()
element = automator.Element(With.javascript("return null"))
cleanup()

setup()
element = automator.Element(With.javascript("return undefined"))
cleanup()

setup()
element = automator.Element(With.javascript("return []"))
cleanup()

setup()
element = automator.Element(With.javascript("return 1"))
cleanup()

setup()
element = automator.Element(With.javascript("return [1,2]"))
cleanup()

automator.quit()