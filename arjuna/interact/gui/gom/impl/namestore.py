
class GuiNameStore:

    def __init__(self):
        # dict<String, GuiNameStore>
        self.__ns_map = {}

    # Needs to be thread safe
    def has_namespace(self, name):
        return name in self.__ns_map

    # loader is GuiNamespaceLoader
    # Needs to be thread safe
    def load_namespace(self, name, loader):
        if not self.has_namespace(name):
            loader.load()
            self.__ns_map[name.lower()] = loader.namespace

        return self.__ns_map[name.lower()]

    # Needs to be thread-safe
    def get_namespace(self, name):
        return self.__ns_map[name.lower()]