
from arjuna import *
from arjex_webui_basics.lib.wp import *

@for_test
def logged_in_wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)