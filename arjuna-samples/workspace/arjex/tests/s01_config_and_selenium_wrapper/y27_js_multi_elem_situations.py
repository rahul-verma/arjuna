from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()

wordpress = None
melement = None

def setup():
    global wordpress
    wordpress = create_wordpress_app()

def cleanup():
    global wordpress
    global melement    
    for i in range(melement.length):
        print(melement[i].source.content.root)
    wordpress.quit()
    melement = None
    wordpress = None

setup()
melement = wordpress.ui.multi_element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
melement = wordpress.ui.multi_element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

# setup()
# melement = wordpress.ui.multi_element(With.javascript("return null"))
# cleanup()

# setup()
# melement = wordpress.ui.multi_element(With.javascript("return [undefined]"))
# cleanup()

# setup()
# melement = wordpress.ui.multi_element(With.javascript("return []"))
# cleanup()

# setup()
# melement = wordpress.ui.multi_element(With.javascript("return 1"))
# cleanup()

# setup()
# melement = wordpress.ui.multi_element(With.javascript("return [document.getElementById('wp-submit'), 2]"))
# cleanup()