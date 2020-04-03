
class GNSFormatter:

    def __init__(self, gns, gui_def, **fargs):
        self.__gns = gns
        self.__gui_def = gui_def
        self.__fargs = fargs

    def __getattr__(self, name):
        emd = self.__gui_def.get_emd(name)
        from arjuna import log_debug
        log_debug("Finding element with label: {}, emd: {} and fargs: {}".format(name, emd, self.__fargs))
        fmt_emd = emd.create_formatted_emd(**self.__fargs)
        return self.__gns.locate_with_emd(fmt_emd)


class WithFormatter:

    def __init__(self, creator, **fargs):
        self.__creator = creator
        self.__fargs = fargs

    def __getattr__(self, factory):
        from functools import partial
        return partial(getattr(self.__creator, factory), fargs=self.__fargs)

