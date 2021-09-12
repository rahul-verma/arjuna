from .group import *
from .module import *
from .test import *

__all__ = [
    # Generic
    "group_resource", 
    "module_resource", 
    "test_resource", 
    "constant_int",

    # GUI Auto
    "wordpress", 
    "logged_in_wordpress",
    "logged_in_wordpress_gns",

    # HTTP Auto
    "httpbin",
    "httpsbin",
    "httpbinseam",
    "httpsbinseam",
    "narada"
]