from commons import *
from arjuna.tpi.guiauto.helpers import With

init_arjuna()

automator = None
element = None

def setup():
    global automator
    automator = launch_automator()
    go_to_wp_home(automator)

def cleanup():
    global automator
    global element
    print(element.source.content.root)
    automator.quit()
    element = None
    automator = None

setup()
element = automator.element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
element = automator.element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

# setup()
# element = automator.element(With.javascript("return null"))
# cleanup()

# setup()
# element = automator.element(With.javascript("return undefined"))
# cleanup()

# setup()
# element = automator.element(With.javascript("return []"))
# cleanup()

# setup()
# element = automator.element(With.javascript("return 1"))
# cleanup()

# setup()
# element = automator.element(With.javascript("return [1,2]"))
# cleanup()
