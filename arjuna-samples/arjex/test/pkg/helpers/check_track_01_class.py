# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna import *

@track
class ClassTrack:

    def __init__(self, a, *vargs, b=None, **kwargs):
        log_debug("in __init__")

    def test1(self, a, *vargs, b=None, **kwargs):
        log_debug("in test1")

    @classmethod
    def cls_method(cls, a):
        log_debug("in cls_method")

    @staticmethod
    def stat_method(a):
        log_debug("in stat_method")

    @property
    def prop1(self):
        log_debug("in prop1 getter")
        return 1

    @prop1.setter
    def prop1(self, a):
        log_debug("in prop1 getter")


@track("info")
class ClassTrackInfo:

    def __init__(self, a, *vargs, b=None, **kwargs):
        log_debug("in __init__")

    def test1(self, a, *vargs, b=None, **kwargs):
        log_debug("in test1")

    @classmethod
    def cls_method(cls, a):
        log_debug("in cls_method")

    @staticmethod
    def stat_method(a):
        log_debug("in stat_method")

    @property
    def prop1(self):
        log_debug("in prop1 getter")

@test
def check_class_track_default_level(request):
    s = ClassTrack(2, 3, 4, b="something", c="dynamic")
    s.test1(5,6, b=13, divmod="whatever")
    s.cls_method(5)
    s.stat_method(6)
    s.prop1


@test
def check_class_track_level(request):
    s = ClassTrackInfo(2, 3, 4, b="something", c="dynamic")
    s.test1(5,6, b=13, divmod="whatever")
    s.cls_method(5)
    s.stat_method(6)
    s.prop1