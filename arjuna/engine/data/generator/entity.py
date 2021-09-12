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

from mimesis import locales as Locales
from mimesis import Person
from mimesis import Address

class Entity:

    @classmethod
    def address(cls, *, 
            locale=Locales.EN,
            calling_code=None, 
            city=None, 
            country=None, 
            country_code=None,
            latitude=None, 
            longitude=None,
            postal_code=None, 
            state=None,
            street_name=None,
            street_number=None,
            street_suffix=None
        ):
        '''
            Create an Address Data Entity object.

            All individual fields are automatically randomly generated based on locale. If provided, the corresponding values are overriden.

            Note:
                All individual fields are randomly generated. Don't expect correct correlation e.g. correct postal code for the generated city.

            Keyword Arguments:
                locale: Approprite Random.locale.<local_name> object. Default is Random.locale.EN
                calling_code: Calling Code
                city: City
                country: Country Name
                country_code: Country Code 
                latitude: Latitude
                longitude: Longitde
                postal_code: Postal Code
                state: State
                street_name: Street Name
                street_number Street Number
                street_suffix: Street Suffix
        '''
        address = Address(locale=locale)
        from arjuna.engine.data.entity.address import Address as ArjAddress

        return ArjAddress(
            calling_code=calling_code is not None and calling_code or address.calling_code(), 
            city=city and city is not None or address.city(), 
            country=country is not None and country or address.country(), 
            country_code=country_code is not None and country_code or address.country_code(), 
            latitude=latitude is not None and latitude or address.latitude(), 
            longitude=longitude is not None and longitude or address.longitude(),
            postal_code=postal_code is not None and postal_code or address.postal_code(), 
            state=state is not None and state or address.state(),
            street_name=street_name is not None and street_name or address.street_name(),
            street_number=street_number is not None and street_number or address.street_number(),
            street_suffix=street_suffix is not None and street_suffix or address.street_suffix(),
        )

    @classmethod
    def person(cls, *, 
            locale=Locales.EN,
            qualification=None,
            age=None,
            blood_type=None,
            email=None,
            first_name=None,
            last_name=None,
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
            work_experience=None,

        ):
        '''
            Create an Person Data Entity object.

            All individual fields are automatically randomly generated based on locale. If provided, the corresponding values are overriden.

            Note:
                All individual fields are randomly generated. Don't expect correct correlation e.g. correct postal code for the generated city.

            Keyword Arguments:
                locale: Approprite Random.locale.<local_name> object. Default is Random.locale.EN
                qualification: Educational Qualification
                age: Age
                blood_type: Blood type
                email: Email address
                first_name: First name
                last_name: Last name
                gender: Gender
                height: Height
                id: Identifier
                language: Language
                nationality: Nationality
                occupation: Occupation
                phone: Phone number
                title: Title
                university: University
                weight: Weight
                work_experience: Work Experience
        '''
        person = Person(locale=locale)
        from arjuna.engine.data.entity.person import Person as ArjPerson

        first_name=first_name is not None and first_name or person.first_name()
        last_name=last_name is not None and last_name or person.last_name()
        return ArjPerson(
            qualification=qualification is not None and qualification or person.academic_degree(),
            age=age is not None and age or person.age(),
            blood_type=blood_type is not None and blood_type or person.blood_type(),
            email=email is not None and email or person.email(),
            first_name=first_name,
            last_name=last_name,
            name=first_name + " " + last_name,
            gender=gender is not None and gender or person.gender(),
            height=height is not None and height or person.height(),
            id=id is not None and id or person.identifier(),
            language=language is not None and language or person.language(),
            nationality=nationality is not None and nationality or person.nationality(),
            occupation=occupation is not None and occupation or person.occupation(),
            phone=phone is not None and phone or person.telephone(),
            title=title is not None and title or person.title(),
            university=university is not None and university or person.university(),
            weight=weight is not None and weight or person.weight(),
            work_experience=work_experience is not None and work_experience or person.work_experience(),
        )


