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

@test(drive_with=
    records(
        # Excel
        record(bucket="eusers", dcontext="bronze", field="user"),
        record(bucket="eusers", dcontext="bronze", field="pwd"), 
        record(bucket="eusers", dcontext="silver", field="user"),
        record(bucket="eusers", dcontext="silver", field="pwd"), 
        record(bucket="eusers", dcontext="gold", field="user"),
        record(bucket="eusers", dcontext="gold", field="pwd"), 

        # Yaml
        record(bucket="yusers", dcontext="bronze", field="user"),
        record(bucket="yusers", dcontext="bronze", field="pwd"), 
        record(bucket="yusers", dcontext="silver", field="user"),
        record(bucket="yusers", dcontext="silver", field="pwd"), 
        record(bucket="yusers", dcontext="gold", field="user"),
        record(bucket="yusers", dcontext="gold", field="pwd"), 
))
def check_contextual_data_ref(request, data):
    # Record
    print(R(bucket=data.bucket, context=data.dcontext))
    print(R(f"{data.dcontext}", bucket=data.bucket))
    print(R(f"{data.bucket}.{data.dcontext}")) 

    # Individual Values
    print(R(f"{data.field}", bucket=data.bucket, context=data.dcontext))
    print(R(f"{data.dcontext}.{data.field}", bucket=data.bucket))
    print(R(f"{data.bucket}.{data.dcontext}.{data.field}")) 

@test(drive_with=
    records(
        # Excel
        record(bucket="eindexed", index=0, field="left"),
        record(bucket="eindexed", index=0, field="right"),
        record(bucket="eindexed", index=0, field="sum"), 
        record(bucket="eindexed", index=1, field="left"),
        record(bucket="eindexed", index=1, field="right"), 
        record(bucket="eindexed", index=1, field="sum"), 

        # Yaml
        record(bucket="yindexed", index=0, field="left"),
        record(bucket="yindexed", index=0, field="right"),
        record(bucket="yindexed", index=0, field="sum"), 
        record(bucket="yindexed", index=1, field="left"),
        record(bucket="yindexed", index=1, field="right"), 
        record(bucket="yindexed", index=1, field="sum"), 
))

def check_indexed_data_ref(request, data):
    print(R(bucket=data.bucket, index=data.index))
    print(R(f"{data.index}", bucket=data.bucket))
    print(R(f"{data.bucket}.{data.index}")) 

    print(R(f"{data.field}", bucket=data.bucket, index=data.index))
    print(R(f"{data.index}.{data.field}", bucket=data.bucket))
    print(R(f"{data.bucket}.{data.index}.{data.field}"))