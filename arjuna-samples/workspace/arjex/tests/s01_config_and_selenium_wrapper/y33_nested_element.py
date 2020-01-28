from commons import *
from arjuna import *

init_arjuna()
wordpress = create_wordpress_app()

# Locate the form and then all input elements
form = wordpress.ui.element(With.id("loginform"))
user_box = form.element(With.tag_name("input"))
print(user_box.source.content.all)
labels = form.multi_element(With.tag_name("label"))
for label in labels:
    print(label.text)
    print(label.source.content.all)
    i = label.element(With.tag_name("input"))
    print(i.source.content.all)

wordpress.quit()