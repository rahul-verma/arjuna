from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

Arjuna.init()
# Default Gui automation engine is Selenium
automator = None
melement = None

def setup():
    global automator
    automator = Arjuna.create_gui_automator(Arjuna.get_central_config())
    go_to_wp_home(automator)

def cleanup():
    for i in range(melement.length):
        print(melement.at_index(i).source.content.root)
    global automator
    global melement
    automator.quit()
    melement = None
    automator = None

setup()
melement = automator.MultiElement(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
melement = automator.MultiElement(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

setup()
melement = automator.MultiElement(With.javascript("return null"))
cleanup()

setup()
melement = automator.MultiElement(With.javascript("return [undefined]"))
cleanup()

setup()
melement = automator.MultiElement(With.javascript("return []"))
cleanup()

setup()
melement = automator.MultiElement(With.javascript("return 1"))
cleanup()

setup()
melement = automator.MultiElement(With.js("return [document.getElementById('wp-submit'), 2]"))
cleanup()

automator.quit()