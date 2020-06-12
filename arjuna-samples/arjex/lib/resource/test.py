
from arjuna import *


@for_test
def test_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}


@for_test
def wordpress(request):
    '''
        For this fixture:
        Wordpress related user options have been added to the project.yaml
        You should replace the details with those corresponding to your own deployment of WordPress.
        user_options {
	        wp.app.url = "IP address"
	        wp.login.url = ${user_options.wp.app.url}"/wp-admin"
        }
    '''

    # Setup
    wp_url = C("wp.login.url")
    wordpress = GuiApp(url=wp_url)
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