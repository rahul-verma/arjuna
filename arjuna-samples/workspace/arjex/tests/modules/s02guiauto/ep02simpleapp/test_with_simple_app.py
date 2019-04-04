from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *
from arjuna.tpi.guiauto import DefaultGui


@test_function
def test(my):

    automator = Arjuna.create_gui_automator()

    # Create Gui. Provide GNS file path
    app = DefaultGui(automator, "WordPress", "simpleapp/WordPress.gns")

    # Login
    app.Browser().go_to_url(automator.get_config().get_user_option_value("wp.login.url").as_string())
    app.Element("login").set_text("user")
    app.Element("password").set_text("bitnami")
    app.Element("submit").click()
    app.Element("view-site").wait_until_clickable()

    # Tweak Settings
    app.Element("settings").click()

    role_select = app.DropDown("role")
    print(role_select.has_visible_text_selected("Subscriber"))
    print(role_select.has_value_selected("subscriber"))
    print(role_select.has_index_selected(2))
    print(role_select.get_first_selected_option_text())
    role_select.select_by_value("editor")
    role_select.select_by_visible_text("Subscriber")
    role_select.select_by_index(4)

    # Logout
    app.Browser().go_to_url(automator.get_config().get_user_option_value("wp.logout.url").as_string())
    app.get_automator().quit()
