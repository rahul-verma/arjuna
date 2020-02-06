

def problem_in(*names):
    def call():
        return names
    return call