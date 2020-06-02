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
def check_excel_contextual_data_ref_value(request):
    print(R("user", bucket="cusers", context="bronze"))
    print(R("bronze.user", bucket="cusers"))
    print(R("cusers.bronze.user"))  

@test
def check_excel_contextual_data_ref_record(request):
    print(R(bucket="cusers", context="bronze"))
    print(R("bronze", bucket="cusers"))
    print(R("cusers.bronze")) 

@test
def check_excel_indexed_data_ref_value(request):
    print(R("left", bucket="indexed", index=1))
    print(R("1.left", bucket="indexed"))
    print(R("indexed.1.left"))

@test
def check_excel_indexed_data_ref_record(request):
    print(R(bucket="indexed", index=1))
    print(R("1", bucket="indexed"))
    print(R("indexed.1")) 