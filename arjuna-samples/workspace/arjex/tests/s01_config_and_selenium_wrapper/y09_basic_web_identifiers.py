from commons import *
from arjuna.tpi.guiauto.helpers import With
from arjuna.tpi.guiauto import WebApp

init_arjuna()
wordpress = create_wordpress_app()

# The following code is for user name field.
# Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
element = wordpress.ui.element(With.id("user_login"))
print(element.source.content.root)

element = wordpress.ui.element(With.name("log"))
print(element.source.content.root)

element = wordpress.ui.element(With.class_name("input"))
print(element.source.content.root)

element = wordpress.ui.element(With.tag_name("input"))
print(element.source.content.root)

# The following options are for 
# Html of link: <a href="http://192.168.56.103/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
element = wordpress.ui.element(With.link_text("Lost your password?"))
print(element.source.content.root)

element = wordpress.ui.element(With.link_ptext("password"))
print(element.source.content.root)

wordpress.quit()
