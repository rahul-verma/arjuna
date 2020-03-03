
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
import os
from .factory import DataReference
from .reference import ContextualDataReference
from arjuna.core.adv.types import CIStringDict

class Localizers:

    def __init__(self):
        vars(self)['_store'] = CIStringDict()

    def __getitem__(self, name):
        return self._store[name]

    def __setitem__(self, name, value):
        self._store[name] = value

    def __getattr__(self, name):
        if type(name) is str and not name.startswith("__"):
            return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __str__(self):
        return str(self._store)

class Localizer:

    def __init__(self, global_map, context_wise):
        self.__globals = global_map
        self.__context_map = context_wise

    @property
    def globals(self):
        return self.__globals

    @property
    def context_map(self):
        return self.__context_map

    @classmethod
    def load_all(cls, ref_config):
        from arjuna.core.enums import ArjunaOption
        l10_excel_dir = ref_config.arjuna_options.value(ArjunaOption.DATA_L10_EXCEL_DIR)
        l10_merged_ref = ContextualDataReference()
        l10_refs = Localizers()
        fnames = os.listdir(l10_excel_dir)
        fnames.sort()
        for fname in fnames:
            if fname.lower().endswith("xls"):
                print(fname)
                ref = DataReference.create_excel_column_data_ref(os.path.join(l10_excel_dir, fname))
                l10_merged_ref.update(ref)
                l10_refs[os.path.splitext(fname)[0]] = ref
        return Localizer(l10_merged_ref, l10_refs)

def L(in_str, *, bucket=None, locale=None):
    from arjuna import Arjuna
    lang = locale and locale.name.lower() or Arjuna.get_ref_config().locale.name.lower()
    if lang != "en":
        if not bucket:
            return Arjuna.get_localizer().globals.record_for(lang)[in_str]
        else:
            return Arjuna.get_localizer().context_map[bucket].record_for(lang)[in_str]
    else:
        return in_str

