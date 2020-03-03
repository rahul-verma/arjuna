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

class Localizer:

    @classmethod
    def load_all(cls, ref_config):
        from arjuna.core.enums import ArjunaOption
        l10_excel_dir = ref_config.arjuna_options.value(ArjunaOption.DATA_L10_EXCEL_DIR)
        l10_ref = ContextualDataReference()
        for fname in os.listdir(l10_excel_dir):
            if fname.lower().endswith("xls"):
                ref = DataReference.create_excel_column_data_ref(os.path.join(l10_excel_dir, fname))
                l10_ref.update(ref)
        return l10_ref


def L(in_str, locale=None):
    from arjuna import Arjuna
    lang = locale and locale.name.lower() or Arjuna.get_ref_config().locale.name.lower()
    if lang != "en":
        return Arjuna.get_localizer().record_for(lang)[in_str]
    else:
        return in_str

