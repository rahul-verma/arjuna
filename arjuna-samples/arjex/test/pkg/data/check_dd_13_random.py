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
        print(s)
        assert len(s) == 36

@test
def check_random_ustr_02(request):
    for i in range(1000):
        s = Random.ustr(prefix="abc")
        print(s)
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
        print(s)
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
        print(s)
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
        print(s)
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
        print(s)
        assert len(s) >= 60
        assert len(s) <=85

@test(xfail=True)
def check_random_ustr_07_error(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=200, maxlen=100)

@test
def check_random_ustr_08(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=24)

@test
def check_random_ustr_09(request):
    s = Random.ustr(prefix="abc", delim="*", minlen=24) # less than base string. reset to base string length

@test(xfail=True)
def check_random_ustr_10_error(request):
    s = Random.ustr(prefix="abc", delim="*", maxlen=24, strict=True) # exception

@test
def check_random_fstr_01(request):
    s = Random.fixed_length_str(length=40)
    print(s)
    assert len(s) == 40

@test
def check_random_class_locale_property_basic(request):
    print(Random.locale)
    print(Random.locale.en)

@test
def check_random_class_locale_property_supported(request):
    print(Random.locale.supported)

@test
def check_random_class_locale_property_objreuse(request):
    id1 = id(Random.locale.en)
    id2 = id(Random.locale.en)
    assert id1 == id2

@test
def check_random_class_local_first_name(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.first_name(locale=locale)))

@test
def check_random_class_local_last_name(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.last_name(locale=locale)))

@test
def check_random_class_local_name(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.name(locale=locale)))


@test
def check_random_class_local_phone(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.phone(locale=locale)))

@test
def check_random_class_local_email(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.email(locale=locale)))

@test
def check_random_class_local_street_name(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.street_name(locale=locale)))

@test
def check_random_class_local_street_number(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.street_number(locale=locale)))

@test
def check_random_class_local_house_number(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.house_number(locale=locale)))

@test
def check_random_class_local_postal_code(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.postal_code(locale=locale)))

@test
def check_random_class_local_city(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.city(locale=locale)))

@test
def check_random_class_local_country(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.country(locale=locale)))

@test
def check_random_class_local_sentence(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.sentence(locale=locale)))

@test
def check_random_class_local_alphabet(request):
    for lname in Random.locale.supported:
        locale = getattr(Random.locale, lname)
        print("{}: {}".format(lname, Random.alphabet(locale=locale)))

@test
def check_random_class_person_1(request):
    print(Random.person())

@test
def check_random_class_address_1(request):
    print(Random.address())

@test
def check_random_class_email_1(request):
    print(Random.email())

@test
def check_random_class_email_2(request):
    print(Random.email(name="test"))

@test
def check_random_class_email_3(request):
    print(Random.email(domain="test.com"))

@test
def check_random_class_email_4(request):
    print(Random.email(name="test", domain="test.com"))

@test
def check_random_class_street_number_1(request):
    print(Random.street_number())

@test
def check_random_class_street_number_2(request):
    print(Random.street_number(prefix="St No."))

@test
def check_random_class_house_number_1(request):
    print(Random.house_number())

@test
def check_random_class_house_number_2(request):
    print(Random.house_number(prefix="H.No."))

@test
def check_random_class_alphabet_1(request):
    print(Random.alphabet())

@test
def check_random_class_alphabet_2(request):
    print(Random.alphabet(lower_case=True))

@test
def check_random_class_file_1(request):
    from arjuna.engine.data.generator.file import File
    for name in vars(File):
        if not name.startswith("__"):
            print(getattr(Random, name)())

@test
def check_random_class_color_1(request):
    print(Random.color())
    print(Random.rgb_color())
    print(Random.hex_color())