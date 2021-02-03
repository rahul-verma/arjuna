# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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
def test1(self, a, *vargs, b=None, **kwargs):
    log_debug("in test1")

@track("info")
def test2(self, a, *vargs, b=None, **kwargs):
    log_debug("in test2")

@test
def check_func_track(request):
    test1(5,6, b=13, divmod="whatever")
    test2(7,8, b=15, divmod="try")