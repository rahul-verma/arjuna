from arjuna.engine.selection.rules.rule import Selector

def get_rule(r):
    selector = Selector()    
    selector.add_rule(r)
    return selector.rules[0]

class Empty:
    pass

class Obj:
    def __init__(self):
        self.properties = Empty()