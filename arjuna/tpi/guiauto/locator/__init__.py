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

from arjuna.tpi.guiauto.helpers import Dictable

class GuiWidgetLocator(Dictable):

    def __init__(self, type="element", fmt_args=None, **named_args):
        self.__widget_type = type

        self.__fmt_args = fmt_args
        if self.__fmt_args is None:
            self.__fmt_args = dict()

        self.__named_args = named_args

        from arjuna.interact.gui.auto.finder.meta import Meta
        self.__meta = Meta({
            "type" : type,
        })

    @property
    def widget_type(self):
        return self.__widget_type

    @property
    def fmt_args(self):
        return self.__fmt_args

    @property
    def named_args(self):
        return self.__named_args

    def __str__(self):
        return str(
            {
                "type": self.widget_type,
                "fmt_args": self.fmt_args,
                "meta": str(self.__meta)
            }
        )

    def _as_raw_wmd(self):
        from arjuna import Arjuna
        from arjuna.interact.gui.auto.finder._with import With
        from arjuna.interact.gui.auto.finder.enums import WithType
        with_list = []
        for k,v in self.__named_args.items():
            if k.upper() in WithType.__members__:
                if isinstance(v, Dictable):
                    v = v.as_dict()
                with_list.append(getattr(With, k.lower())(v))
            elif Arjuna.get_withx_ref().has_locator(k):
                if isinstance(v, Dictable):
                    v = v.as_dict()
                    with_list.append(getattr(With, k.lower())(**v))
                else:
                    with_list.append(getattr(With, k.lower())(v))
            else:
                self.__meta[k] = v
        if not with_list:
            raise Exception("You must provide atleast one locator.")
        from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
        return GuiWidgetMetaData.create_wmd(*with_list, meta=self.__meta)

    def as_wmd(self):
        wmd = self._as_raw_wmd()
        fmt_wmd = wmd.create_formatted_wmd(**self.__fmt_args)
        return fmt_wmd