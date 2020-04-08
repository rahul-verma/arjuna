
class GNSFormatter:

    def __init__(self, gns, gui_def, **fargs):
        self.__gns = gns
        self.__gui_def = gui_def
        self.__fargs = fargs

    def __getattr__(self, name):
        wmd = self.__gui_def.get_wmd(name)
        from arjuna import log_debug
        log_debug("Finding element with label: {}, wmd: {} and fargs: {}".format(name, wmd, self.__fargs))
        fmt_wmd = wmd.create_formatted_wmd(**self.__fargs)
        return self.__gns.locate_with_wmd(fmt_wmd)


class WithFormatter:

    def __init__(self, creator, **fargs):
        self.__creator = creator
        self.__fargs = fargs

    def __getattr__(self, factory):
        from functools import partial
        return partial(getattr(self.__creator, factory), fargs=self.__fargs)

