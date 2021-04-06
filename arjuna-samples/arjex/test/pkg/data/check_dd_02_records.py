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

msg="Unexpected data record."

@test(drive_with=
    records(
        record(1,2,sum=3),    # Pass
        record(4,5,sum=9),    # Pass
        record(7,8,sum=10),   # Fail
    )
)
def check_records_ascii(request, data):
    request.asserter.assert_equal(data[0] + data[1], data['sum'], msg=msg)


@test(drive_with=
    records(
        record("non ascii chars ÄÖÜ@€!§$%/()=?``"),
        record("some utf-8 chars \U0001f408 \u00B5 \U0001F431"),    # Pass
        record("some utf-8 chars Δ"),   # Fail
    )
)
def check_records_spchars(request, data):
    print(data)


@test(drive_with=
    records(
        record(whatever=str(generator(
                        Random.ustr, 
                        prefix='with non ascii chars ÄÖÜ@€!§$%/()=?``', 
                        maxlen=50
                ).generate())
        )
    )
)
def check_records_data_entity(request, data):
    print(data)

@test(drive_with=
    records(
        record(whatever=str(generator(
                        Random.ustr, 
                        prefix='with non ascii chars ÄÖÜ@€!§$%/()=?``', 
                        maxlen=50
                ).generate())
        )
    )
)
def check_records_random_data_entity(request, data):
    print(data)