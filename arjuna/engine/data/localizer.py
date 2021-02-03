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


import os
from .factory import DataReference
from .reference import ContextualDataReference
from arjuna.tpi.helper.arjtype import CIStringDict

from arjuna.core.utils import file_utils
from arjuna.tpi.parser.json import Json, JsonDict

class L10NRef:

    def __init__(self, ref_config):
        self.map = {}
        self.ref_config = ref_config

    def update_from_excel_ref(self, localizer_ref):
        for lang, record in localizer_ref.map.items():
            if lang not in self.map:
                self.map[lang] = JsonDict()
            self.map[lang].update(record.named_values)

    def update_from_json_ref(self, json_ref):
        for lang, map in json_ref.map.items():
            if lang not in self.map:
                self.map[lang] = JsonDict()
            self.map[lang].update(map)

    def lang(self, lang):
        if lang.lower() in self.map:
            return self.map[lang.lower()]
        else:
            raise Exception("Language key {} not found in localizer: {}.".format(lang, self.__class__.__name__))

    def __str__(self):
        return str({k: str(v) for k,v in self.map.items()})

    def enumerate(self):
        for k,v in self.map.items():
            print(k, "::", type(v), str(v))

    def get_localizer_file_path(self, ldir, fpath):
        if file_utils.is_absolute_path(fpath):
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
            return fpath
        else:
            fpath = os.path.abspath(os.path.join(ldir, fpath))
            if not file_utils.is_file(fpath):
                if file_utils.is_dir(fpath):
                    raise Exception("Not a file: {}".format(fpath))
                else:
                    raise Exception("File does not exist: {}".format(fpath))
            return fpath

class ExcelL10NRef(L10NRef):

    def __init__(self, ref_config, fpath):
        super().__init__(ref_config)
        excel_ref = DataReference.create_contextual_data_ref(self.ref_config, fpath)
        self.map = excel_ref._map

class JsonL10NRef(L10NRef):

    def __init__(self, ref_config, ldir):
        from arjuna import log_fatal
        super().__init__(ref_config)
        fnames = os.listdir(ldir)
        fnames.sort()
        for fname in fnames:
            if fname.lower().endswith(".json"):
                lang = os.path.splitext(fname)[0].replace("-","_").lower()
                fpath = self.get_localizer_file_path(ldir, fname)
                try:
                    lang_map = Json.from_file(fpath)
                except Exception as e:
                    log_fatal("Error in processing l10n file: {}".format(fpath))
                    log_fatal("Error message: {}".format(str(e)))
                    import traceback
                    log_fatal("Trace: {}".format(traceback.format_exc()))
                    raise
                self.map[lang] = lang_map

class Localizers:

    def __init__(self):
        vars(self)['_store'] = CIStringDict()

    def keys(self):
        return self._store.keys()

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

    def has(self, name):
        return name.lower() in self._store

class Localizer:

    def __init__(self, global_map, buckets):
        self.__globals = global_map
        self.__buckets = buckets     
        self.__bucket_names = self.__buckets.keys()

    @property
    def globals(self):
        return self.__globals

    @property
    def buckets(self):
        return self.__buckets

    @property
    def bucket_names(self):
        return self.__bucket_names

    @classmethod
    def __process_json_ref(cls, l10n_merged_ref, l10n_refs, json_ref, bucket="root"):
        # Check this logic for locale conversion.
        l10n_merged_ref.update_from_json_ref(json_ref)
        if not l10n_refs.has(bucket):
            l10n_refs[bucket] = json_ref

    @classmethod
    def load_all(cls, ref_config):
        from arjuna.tpi.constant import ArjunaOption
        l10n_dir = ref_config.value(ArjunaOption.L10N_DIR)
        l10n_merged_ref = L10NRef(ref_config)
        l10n_refs = Localizers()
        if os.path.isdir(l10n_dir):
            fnames = os.listdir(l10n_dir)
            fnames.sort()
            for fname in fnames:
                if fname.lower().endswith("xls"):
                    ref = ExcelL10NRef(ref_config, os.path.join(l10n_dir, fname))
                    l10n_merged_ref.update_from_excel_ref(ref)
                    l10n_refs[os.path.splitext(fname)[0]] = ref

        if os.path.isdir(l10n_dir):        
            json_ref = JsonL10NRef(ref_config, l10n_dir)
            cls.__process_json_ref(l10n_merged_ref, l10n_refs, json_ref, bucket="root")
            buckets = os.listdir(l10n_dir)
            for bucket in buckets:
                if os.path.isdir(os.path.join(l10n_dir, bucket)):
                    dpath = os.path.join(l10n_dir, bucket)
                    json_ref = JsonL10NRef(ref_config, dpath)
                    cls.__process_json_ref(l10n_merged_ref, l10n_refs, json_ref, bucket=bucket)

        # l10n_merged_ref.enumerate()
        return Localizer(l10n_merged_ref, l10n_refs)

def L(in_str, *, locale=None, bucket=None, strict=None):
    from arjuna import Arjuna, ArjunaOption
    bucket = bucket
    query = in_str
    if bucket is None:
        if in_str.find('.') != -1:
            bucket, query = in_str.split('.', 1)
            bucket = bucket.lower()
            if bucket not in Arjuna.get_localizer().bucket_names:
                bucket = None
                query = in_str
        else:
            query = in_str
    lang = locale and locale.name.lower() or Arjuna.get_config().l10n_locale.name.lower()
    try:
        if not bucket:
            val = Arjuna.get_localizer().globals.lang(lang)[query]
        else:
            val = Arjuna.get_localizer().buckets[bucket].lang(lang)[query]
        if not val:
            raise Exception("No localized string found for: {} for Locale.{}".format(in_str, lang.upper()))
        else:
            return val
    except Exception as e:
        if strict is None:
            strict_mode = Arjuna.get_config().value(ArjunaOption.L10N_STRICT)
        else:
            strict_mode = strict

        if strict_mode:
            import traceback
            raise Exception("Error in retrieving localized string for: {}. {}. {}".format(in_str, str(e), traceback.format_exc()))
        else:
            return in_str
