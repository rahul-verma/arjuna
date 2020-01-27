from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()

wordpress = None
element = None

def setup():
    global wordpress
    wordpress = create_wordpress_app()

def cleanup():
    global wordpress
    global element
    print(element.source.content.root)
    wordpress.quit()
    element = None
    wordpress = None

setup()
element = wordpress.ui.element(With.javascript("return document.getElementById('wp-submit')"))
cleanup()

setup()
element = wordpress.ui.element(With.javascript("return document.getElementsByClassName('input')"))
cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return null"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return undefined"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return []"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return 1"))
# cleanup()

# setup()
# element = wordpress.ui.element(With.javascript("return [1,2]"))
# cleanup()
