
from arjuna import *

@for_test
def wordpress(request):
    '''
        For this fixture:
        Wordpress related user options have been added to the project.conf
        You should replace the details with those corresponding to your own deployment of WordPress.
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
    '''

    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()


from arjex.lib.procedural.wp import *


@for_test
def logged_in_wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)


from arjex.lib.procedural.wp_gns import *


@for_test
def logged_in_wordpress_gns(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)