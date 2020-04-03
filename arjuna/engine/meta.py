
from arjuna.tpi.engine.asserter import Asserter

class Info:

    def __init__(self, pytest_request):
        self.__request = pytest_request
        rnode = self.__request.node
        self.__node_name = rnode.name
        if self.__request.scope == "module":
            self.__orig_name = rnode.name
        elif self.__request.scope == "function":
            self.__orig_name = rnode.originalname and rnode.originalname or rnode.name

    def get_qual_name(self, with_params=False):
        # if pytest name has params only then originalname is set else it is None
        if self.__request.scope in {"module", "session"}:
            return self.__node_name
        else:
            name = with_params and self.__node_name or self.__orig_name
            return self.__request.module.__name__ + "." + name

    def get_qual_name_with_data(self):
        qname = self.get_qual_name(with_params=True)
        if self.__request.fixturename:
            return qname + ":" + self.__request.fixturename
        else:
            return qname

    def __getattr__(self, name):
        return getattr(self.__request, name)

_LOOKUP_ORDER = {
    "session" : ("session", ),
    "module" : ("session", "module"),
    "class" : ("function", "cls", "module"),
    "function" : ("function", "cls", "module", "session")
}

_SCOPE_MAP = {
    "function" : "function",
    "class"    : "cls",
    "module"   : "module",
    "session"  : "session"
}

class Space:

    def __init__(self, pytest_request):
        vars(self)['_request'] = pytest_request
        try:
            config = self.arj_config
        except:
            from arjuna import Arjuna
            self.arj_config = Arjuna.get_config()

    def __getitem__(self, name):
        scopes = _LOOKUP_ORDER[self._request.scope]
        from arjuna import Arjuna
        for scope in scopes:
            Arjuna.get_logger().debug("Space: Getting value for {} from {} scope".format(name, scope))
            try:
                container = getattr(self._request, _SCOPE_MAP[scope])
                return getattr(container, name)
            except Exception as e:
                Arjuna.get_logger().debug("Space: No value for {} in {} scope".format(name, scope))
                continue
        raise Exception("Attribute with name >>{}<< does not exist in request scope for {}".format(name, scopes))

    def _get_container_for_scope(self):
        return getattr(self._request, _SCOPE_MAP[self._request.scope])

    def __setitem__(self, name, value):
        container = self._get_container_for_scope()
        setattr(container, name, value)

    def __getattr__(self, name):
        if type(name) is str and not name.startswith("__"):
            return self[name]

    def __setattr__(self, name, value):
        container = self._get_container_for_scope()
        from arjuna import Arjuna
        Arjuna.get_logger().debug("Space: Setting {}={} in {} scope".format(name, value, self._request.scope))
        setattr(container, name, value)

    @property
    def raw_request(self):
        return self._request

class ModuleSpace(Space):

    def __init__(self, pytest_request):
        super().__init__(pytest_request)

    def _get_container_for_scope(self):
        return getattr(self._request, "module")

class Module:

    def __init__(self, py_request):
        self._space = ModuleSpace(py_request)

    @property
    def space(self):
        return self._space

class My:

    def __init__(self):
        self._data = None
        self._info = None
        self._handler = None
        self._qual_name = None
        self._request =  None
        self._shared_objects = None
        self._asserter = Asserter() #unittest.TestCase('__init__')
        self._space = None
        self._module = None

    @property
    def config(self):
        return self.space.arj_config

    def get_config(self, name=None):
        if name is None:
            return self.config
        else:
            from arjuna import Arjuna
            return Arjuna.get_config(name)
    
    @property
    def data_refs(self):
        from arjuna import Arjuna
        return Arjuna.get_data_references()

    @property
    def module(self):
        return self._module

    @property
    def data(self):
        return self._data

    @property
    def asserter(self):
        return self._asserter

    @data.setter
    def data(self, record):
        self._data = record

    @property
    def space(self):
        return self._space

    def set_req_obj(self, pytest_request):
        self._request = pytest_request
        self._info = Info(pytest_request)
        self._space = Space(pytest_request)
        if pytest_request.scope in {"function"}:
            if not self._module:
                self._module = Module(pytest_request)          

    @property
    def info(self):
        return self._info

    @property
    def resources(self):
        return self._resources

    @property
    def raw_request(self):
        return self._request