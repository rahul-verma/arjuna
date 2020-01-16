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
    global melement    
    for i in range(melement.length):
        print(melement.at_index(i).source.content.root)
    automator.quit()
    melement = None
    automator = None

setup()
melement = automator.multi_element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
melement = automator.multi_element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

# setup()
# melement = automator.multi_element(With.javascript("return null"))
# cleanup()

# setup()
# melement = automator.multi_element(With.javascript("return [undefined]"))
# cleanup()

# setup()
# melement = automator.multi_element(With.javascript("return []"))
# cleanup()

# setup()
# melement = automator.multi_element(With.javascript("return 1"))
# cleanup()

# setup()
# melement = automator.multi_element(With.javascript("return [document.getElementById('wp-submit'), 2]"))
# cleanup()