from arjuna.engine.selection.rules.rule import Selector

def get_rule(r):
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    return rule
    
class Empty:
    pass

class Obj:
    def __init__(self):
        self.info = Empty()
        self.tags = set()
        self.bugs = set()
        self.envs = set()