from arjuna import *

@test
def check_arjuna_action(request, narada):
    narada.action.ditem_create.perform()

