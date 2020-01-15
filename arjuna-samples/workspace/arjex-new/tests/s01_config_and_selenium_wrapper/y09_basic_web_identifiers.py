from commons import *
from arjuna.tpi.guiauto.helpers import With

init_arjuna()

automator = launch_automator()
go_to_wp_home(automator)

# The following code is for user name field.
# Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
element = automator.Element(With.id("user_login"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.name("log"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.class_name("input"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.tag_name("input"))
element.identify()
print(element.source.content.root)

# The following options are for 
# Html of link: <a href="http://192.168.56.103/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
element = automator.Element(With.link_text("Lost your password?"))
element.identify()
print(element.source.content.root)

element = automator.Element(With.link_ptext("password"))
element.identify()
print(element.source.content.root)

automator.quit()
