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


from arjuna.core.adv.types import CIStringDict

class Meta:

    def __init__(self, mdict=None):
        self.__mdict = not mdict and CIStringDict() or CIStringDict(mdict)
        from arjuna.core.enums import GuiTemplate
        if "template" in self.__mdict:
            try:
                template = self.__mdict["template"]
                self.__template = GuiTemplate[template.upper()]
            except:
                raise Exception("{} is not a valid template type.".format(template))
        else:
            self.__template = GuiTemplate.ELEMENT

    def items(self):
        return self.__mdict.items()

    @property
    def template(self):
        return self.__template

    def __str__(self):
        return str(self.__mdict)