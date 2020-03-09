'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna import *

@test
def check_excel_localizer(request):
    print(L("test")) # Default Locale in Config
    print(L("qual", locale=Locale.HI))
    print(L("qual", locale=Locale.EN))

    print(L("corr")) # From global l10 container

    print(L("corr", bucket="sample1")) # From sample1 excel file (bucket)
    print(L("corr", bucket="sample2")) # From sample2 excel file (bucket)

    print(L("sample1.corr")) # From sample1 excel file (bucket)
    print(L("sample2.corr")) # From sample2 excel file (bucket)

@test
def check_json_localizer(request):
    print(L("error.data.lastTransfer", locale=Locale.EN_GB)) # From global l10 container
    print(L("error.data.lastTransfer", locale=Locale.DE_DE)) # From global l10 container

    print(L("error.data.lastTransfer", locale=Locale.EN_GB, bucket="bucket2")) # From bucket2    
    print(L("bucket2.error.data.lastTransfer", locale=Locale.EN_GB)) # From bucket2

    print(L("address.coordinates", locale=Locale.EN_GB))
    print(L("address.coordinates", locale=Locale.EN_GB, bucket="root"))
    print(L("root.address.coordinates", locale=Locale.EN_GB))

@test
def check_strict_l10_mode(request):
    print(L("non_existing"))
    print(L("non_existing", strict=True, locale=Locale.DE_DE))
