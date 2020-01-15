
'''
import logging
import sys
import inspect
import time

from arjuna.interact.gui.auto.automator.guiautomator import GuiAutomator
from arjuna.interact.gui.auto.locator.emd import GuiElementMetaData, SimpleGuiElementMetaData
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


    @classmethod
    def get_logger(cls):
        return cls.LOGGER and cls.LOGGER or cls.__DUMMY_LOGGER


__all__ = ["Setu", "GuiAutomator", "GuiElementMetaData", "SimpleGuiElementMetaData"]
'''