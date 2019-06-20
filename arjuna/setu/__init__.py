import logging
import sys
import inspect
import time

from arjuna.setuext.guiauto.impl.automator.guiautomator import GuiAutomator
from arjuna.setuext.guiauto.impl.locator.emd import GuiElementMetaData, SimpleGuiElementMetaData
from functools import partial

class _DummyLogger:

    def dummy(self, item, *vargs):
        print("Dummy call", item)
        frame = inspect.stack()[3]
        caller_str = "{}.py:{}:L{}".format(inspect.getmodule(frame[0]).__name__, frame[3], frame[2])
        print("Dummy logger called by {} with args: ".format(caller_str), str(vargs)[:300], "...")
        pass

    def __getattr__(self, item):
        return partial(self.dummy, item)


class Setu:
    LOGGER = None
    __DUMMY_LOGGER = _DummyLogger()

    @classmethod
    def init_logger(cls, testsession_id, log_dir):
        logger = logging.getLogger("setu")
        logger.setLevel(logging.DEBUG)
        # ch = logging.StreamHandler(sys.stdout)
        # ch.setLevel(logging.INFO)
        fh = logging.FileHandler(log_dir + "/arjuna-setu-{}-ts-{}.log".format(time.time(), testsession_id), "w", 'utf-8')
        fh.setLevel(logging.DEBUG)
        f_fmt = logging.Formatter(u'[%(levelname)5s]\t%(asctime)s\t%(pathname)s::%(module)s.%(funcName)s:%(lineno)d\t%(message)s')
        c_fmt = logging.Formatter(u'[%(levelname)5s]\t%(message)s')
        # ch.setFormatter(c_fmt)
        fh.setFormatter(f_fmt)
        # logger.addHandler(ch)
        logger.addHandler(fh)
        cls.LOGGER = logger

    @classmethod
    def get_logger(cls):
        return cls.LOGGER and cls.LOGGER or cls.__DUMMY_LOGGER


__all__ = ["Setu", "GuiAutomator", "GuiElementMetaData", "SimpleGuiElementMetaData"]