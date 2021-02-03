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

from arjuna.tpi.helper.arjtype import Dictable
from arjuna.tpi.tracker import track

@track("trace")
class GuiWidgetDefinition(Dictable):
    '''
        Representation of indentifiers, format arguments, widget configuration and named arguments for a GuiWidget.

        Keyword Arguments:
            type: type of GuiWidget. Default is 'element'/GuiWidgetType.ELEMENT. 
            fmt_args: Dictionary of key-value pairs to format the identifiers.
            **named_args: Named arguments representing allowed identifiers, extended identifiers, configuration options and GuiWidget arguments.
    '''

    def __init__(self, *, type="element", fmt_args=None, **named_args):
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
        '''
            Type of this GuiWidget.
        '''
        return self.__widget_type

    @property
    def fmt_args(self):
        '''
            Dictionary of key-value pairs to format the identifiers.
        '''
        return self.__fmt_args

    @property
    def named_args(self):
        '''
            Named arguments representing allowed identifiers, extended identifiers, configuration options and GuiWidget arguments.
        '''
        return self.__named_args

    def __str__(self):
        return str(self.as_dict())

    def _as_dict(self):
        return {
                "type": self.widget_type,
                "fmt_args": self.fmt_args,
                "meta": str(self.__meta)
            }

    def _as_raw_wmd(self):
        from arjuna import Arjuna, oneof, log_debug
        from arjuna.interact.gui.auto.finder._with import With
        from arjuna.interact.gui.auto.finder.enums import WithType

        def add_to_list(with_list, k, v):
            if k.upper() in WithType.__members__:
                if isinstance(v, Dictable):
                    v = v.as_dict()
                with_list.append(getattr(With, k.lower())(v))
            elif Arjuna.get_withx_ref().has_locator(k):
                if isinstance(v, Dictable):
                    v = v.as_dict()
                    with_list.append(getattr(With, k.lower())(**v))
                elif type(v) in {list, tuple}:
                    with_list.append(getattr(With, k.lower())(*v))
                else:
                    with_list.append(getattr(With, k.lower())(v))
            else:
                self.__meta[k] = v

        with_list = []
        for k,v in self.__named_args.items():
            if isinstance(v, oneof):
                for oneofval in v.as_list():
                    add_to_list(with_list, k, oneofval)
            else:
                add_to_list(with_list, k, v)

        if not with_list:
            from arjuna.tpi.error import GuiWidgetDefinitionError
            raise GuiWidgetDefinitionError("You must provide atleast one valid locator argument to create GuiWidgetDefinition definition. None of Arjuna defined locators or withx locators were provided. Got the speification dictionary as: {}".format(self.__named_args))
        from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData

        return GuiWidgetMetaData.create_wmd(*with_list, meta=self.__meta)

    def _as_wmd(self):
        '''
            Convert this **GuiWidgetDefinition** to **GuiWidgetMetaData** object
        '''
        wmd = self._as_raw_wmd()
        from arjuna import log_debug
        log_debug("Unformatted Widget def is: " + str(wmd))
        fmt_wmd = wmd.create_formatted_wmd(**self.__fmt_args)
        return fmt_wmd