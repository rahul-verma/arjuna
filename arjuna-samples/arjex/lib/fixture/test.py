
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


@for_test
def logged_in_wordpress(request):
    from arjex.lib.app_procedural.wp import create_wordpress_app, login, logout
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)


@for_test
def logged_in_wordpress_gns(request):
    from arjex.lib.app_procedural.wp_gns import create_wordpress_app, login, logout
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)