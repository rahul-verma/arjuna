from arjuna import *

@test
def check_ext_dep_dir(request):
    print(C("project.root.dir"))
    print(C("deps.dir"))
    from sample.mod import hello
    hello()