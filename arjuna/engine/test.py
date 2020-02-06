from arjuna.core.utils import obj_utils
import functools
import pytest

def get_test_qual_name(self, request, with_params=True):
    # if pytest name has params only then originalname is set else it is None
    orig_name = request.node.originalname and request.node.originalname or request.node.name
    name = with_params and request.node.name or orig_name
    return obj_utils.get_class_qual_name(self) + "." + name

def tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def call_func(func, self, request, *args, **kwargs):
    from arjuna import Arjuna
    qual_name = self.get_test_qual_name(request)
    Arjuna.get_logger().info("Begin test function: {}".format(qual_name))            
    func(self, request, *args, **kwargs)
    Arjuna.get_logger().info("End test function: {}".format(qual_name))
        
def simple_dec(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        call_func(func, self, request, *args, **kwargs)
    return wrapper

def tm(f=None, *, id=None, drive_with=None, exclude_if=None):
    if f is not None:
        return simple_dec(f)

    def format_test_func(func):
        print(func, exclude_if and exclude_if())
        orig_func = func
        if exclude_if:
            func = pytest.mark.dependency(name=id, depends=exclude_if())(func)
        else:
            func = pytest.mark.dependency(name=id)(func)

        if drive_with:
            func = pytest.mark.parametrize(*drive_with())(func) 

        @functools.wraps(orig_func)
        def wrapper(self, request, *args, **kwargs):
            call_func(func, self, request, *args, **kwargs)
        return wrapper
    
    return format_test_func

    

