
class SourceContent:

    def __init__(self, src):
        self.__src = src

    @property
    def src(self):
        return self.__src

    @property
    def root(self):
        return self.src.get_root_content()

    @property
    def all(self):
        return self.src.get_full_content()

    @property
    def inner(self):
        return self.src.get_inner_content()

    @property
    def text(self):
        return self.src.get_text_content()

class DefaultGuiSource:

    def __init__(self, automator, src):
        self.__automator = automator
        self.__content =  SourceContent(src)

    # @staticmethod
    # def define_source(self, automator, *args):
    #     return DefaultGuiSource(automator, args)

    @property
    def content(self):
        return self.__content


