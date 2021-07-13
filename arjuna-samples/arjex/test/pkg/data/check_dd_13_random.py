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

@test
def check_random_ustr_01(request):
    for i in range(100):
        s = Random.ustr()
        assert len(s) == 36

@test
def check_random_ustr_02(request):
    for i in range(1000):
        s = Random.ustr(prefix="abc")
        assert len(s) == 40

@test
def check_random_ustr_03(request):
    for i in range(1000):
        s = Random.ustr(prefix="abc", delim="*")
        assert len(s) == 40
        s = Random.ustr(prefix="abc", delim="***")
        assert len(s) == 42
        s = Random.ustr(delim="***")
        assert len(s) == 36 # delim is ignored if prefix is not defined.

@test
def check_random_ustr_04(request):
    for i in range(1000):
        s = Random.ustr(minlen=17) # less than half of base string
        assert len(s) >= 17
        assert len(s) <= 36

        s = Random.ustr(minlen=18) # == half of base string
        assert len(s) >= 18
        assert len(s) <= 36

        s = Random.ustr(minlen=19) # > half of base string
        assert len(s) >= 19
        assert len(s) <= 38

        s = Random.ustr(minlen=19, prefix="abc", delim="*") # less than half of base string
        assert len(s) >= 19
        assert len(s) <= 40

        s = Random.ustr(minlen=20, prefix="abc", delim="*") # == half of base string
        assert len(s) >= 20
        assert len(s) <= 40

        s = Random.ustr(minlen=21, prefix="abc", delim="*") # > half of base string
        assert len(s) >= 21
        assert len(s) <= 42

        s = Random.ustr(minlen=71) # less than twice of base string
        assert len(s) >= 71
        assert len(s) <= 142

        s = Random.ustr(minlen=72) # == twice of base string
        assert len(s) >= 72
        assert len(s) <= 144

        s = Random.ustr(minlen=73) # > twice of base string
        assert len(s) >= 73
        assert len(s) <= 146

        s = Random.ustr(minlen=79, prefix="abc", delim="*") # less than twice of base string
        assert len(s) >= 79
        assert len(s) <= 79 * 2

        s = Random.ustr(minlen=80, prefix="abc", delim="*") # == twice of base string
        assert len(s) >= 80
        assert len(s) <= 80 * 2

        s = Random.ustr(minlen=81, prefix="abc", delim="*") # > twice of base string
        assert len(s) >= 81
        assert len(s) <= 81 * 2

@test
def check_random_ustr_05(request):
    for i in range(1000):
        s = Random.ustr(maxlen=35) # < base string
        assert len(s) <= 35
        s = Random.ustr(maxlen=36) # = base string
        assert len(s) <= 36
        s = Random.ustr(maxlen=37) # > base string
        assert len(s) <= 37

        s = Random.ustr(prefix="abc", delim="*", maxlen=39) # < base string
        assert len(s) <= 39
        s = Random.ustr(prefix="abc", delim="*", maxlen=40) # = base string
        assert len(s) <= 40
        s = Random.ustr(prefix="abc", delim="*", maxlen=41) # > base string
        assert len(s) <= 41

@test
def check_random_ustr_06(request):
    for i in range(1000):
        s = Random.ustr(prefix="abc", delim="*", minlen=60, maxlen=85)
        assert len(s) >= 60
        assert len(s) <=85

@test
def check_random_ustr_07_error(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=200, maxlen=100)

@test
def check_random_ustr_08(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=24)

@test
def check_random_ustr_09(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=24) # less than base string. reset to base string length

@test
def check_random_ustr_10_error(request):
    s = Random.ustr(prefix="abc", delim="*", maxlen=24, strict=True) # exception

@test
def check_random_fstr_01(request):
    s = Random.fixed_length_str(length=40)
    print(s)
    assert len(s) == 40


