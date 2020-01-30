'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
import logging
import sys
import inspect
import time

from arjuna.interact.gui.auto.automator.guiautomator import GuiAutomator
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData, SimpleGuiElementMetaData
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