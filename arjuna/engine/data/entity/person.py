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

from arjuna.tpi.data.entity import data_entity

Person = data_entity(
        "Person", 
        qualification=None,
        age=None,
        blood_type=None,
        email=None,
        first_name=None,
        last_name=None,
        name=None,
        gender=None,
        height=None,
        id=None,
        language=None,
        nationality=None,
        occupation=None,
        phone=None,
        title=None,
        university=None,
        weight=None,
        work_experience=None
    )