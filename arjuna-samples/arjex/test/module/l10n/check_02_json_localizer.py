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

@test
def check_json_localizer(request):
    print(L("error.data.lastTransfer", locale=Locale.EN_GB)) # From global l10n container
    print(L("error.data.lastTransfer", locale=Locale.DE_DE)) # From global l10n container

    print(L("error.data.lastTransfer", locale=Locale.EN_GB, bucket="bucket2")) # From bucket2    
    print(L("bucket2.error.data.lastTransfer", locale=Locale.EN_GB)) # From bucket2

    print(L("address.coordinates", locale=Locale.EN_GB))
    print(L("address.coordinates", locale=Locale.EN_GB, bucket="root"))
    print(L("root.address.coordinates", locale=Locale.EN_GB))
