
from arjuna.tpi.engine.asserter import Asserter

class Info:

    def __init__(self, pytest_request, attrs=None):
        self.__attrs = attrs
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
        if name in self.__attrs:
            return self.__attrs[name]
        else:
            try:
                return getattr(self.__request, name)
            except:
                raise Exception("{name} is not a valid test information attribute. Built-in Arjuna attributes: {attrs}".format(name=name, attrs=str(self.__attrs)))

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
        from arjuna import log_trace
        for scope in scopes:
            log_trace("Space: Getting value for {} from {} scope".format(name, scope))
            try:
                container = getattr(self._request, _SCOPE_MAP[scope])
                return getattr(container, name)
            except Exception as e:
                log_trace("Space: No value for {} in {} scope".format(name, scope))
                continue
        raise Exception("Attribute with name >>{}<< does not exist in request scope for {}".format(name, scopes))

    def _get_container_for_scope(self):
        return getattr(self._request, _SCOPE_MAP[self._request.scope])

    def __setitem__(self, name, value):
        container = self._get_container_for_scope()
        setattr(container, name, value)

    def __getattr__(self, name):
        from arjuna import log_trace
        if type(name) is str and not name.startswith("__"):
            try:
                val = self[name]
                log_trace("Space: Got value {} for {}.".format(val, name))
                return val
            except Exception as e:
                log_trace("Space: No value for {} in {} in any scope.".format(name))
                raise AttributeError(str(e))

    def __setattr__(self, name, value):
        container = self._get_container_for_scope()
        from arjuna import log_trace
        log_trace("Space: Setting {}={} in {} scope".format(name, value, self._request.scope)) #, contexts="request")
        setattr(container, name, value)

    @property
    def raw_request(self):
        return self._request

class GroupSpace(Space):

    def __init__(self, pytest_request):
        super().__init__(pytest_request)

    def _get_container_for_scope(self):
        return getattr(self._request, "session") # Each Arjuna group represents a Pytest session in a thread.

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

class Group:

    def __init__(self, py_request):
        self._space = GroupSpace(py_request)
        self._info = py_request.session.group_info

    @property
    def space(self):
        return self._space

    @property
    def thread_name(self):
        return self._info.thread_name

    @property
    def name(self):
        return self._info.name

    @property
    def config(self):
        return self._info.config

class My:

    def __init__(self, test_meta_data=None):
        self._data = None
        self._info = None
        self._handler = None
        self._qual_name = None
        self._request =  None
        self._shared_objects = None
        self._asserter = Asserter() #unittest.TestCase('__init__')
        self._space = None
        self._module = None
        self._attrs = None
        self._tags = None
        self._bugs = None
        self._envs = None
        if test_meta_data:
            self._attrs = test_meta_data['info']
            if self._attrs['id'] is None:
                self._attrs['id'] = self._attrs['qual_name']
            self._tags = test_meta_data['tags']
            self._bugs = test_meta_data['bugs']
            self._envs = test_meta_data['envs']
        self._group = None

    @property
    def config(self):
        return self.space.arj_config

    @property
    def tags(self):
        return self._tags

    @property
    def bugs(self):
        return self._bugs

    @property
    def envs(self):
        return self._envs

    def get_config(self, name=None):
        if name is None:
            return self.config
        else:
            from arjuna import Arjuna
            return Arjuna.get_config(name)
    
    @property
    def contextual_data_refs(self):
        from arjuna import Arjuna
        return Arjuna.get_data_references()

    @property
    def group(self):
        '''
            This info is available only within the body of a fixture or test function.
        '''
        # By this stage the Arjuna's built-in default group fixture has executed and group_info is available as pytest_request.session.group_info
        if not self._group:
            self._group = Group(self._request)
        return self._group

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
        self._info = Info(pytest_request, self._attrs)
        self._space = Space(pytest_request)
        if pytest_request.scope in {"function"}:
            if not self._module:
                self._module = Module(pytest_request)  
            if not self._group:
                self._group = Group(self._request)   
        if pytest_request.scope in {"module"}:
            if not self._group:
                self._group = Group(self._request)  

    @property
    def info(self):
        return self._info

    @property
    def resources(self):
        return self._resources

    @property
    def raw_request(self):
        return self._request