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

class Page:

    def __init__(self, *args, source_gui, label=None, gns_dir=None, gns_file_name=None, **kwargs):
        from arjuna.interact.gui.gom import Page
        label = label and label or self.__class__.__name__
        self.__page = Page(*args, source_gui=source_gui, label=label, gns_dir=gns_dir, gns_file_name=gns_file_name, **kwargs)

    def __getattr__(self, name):
        return getattr(self.__page, name)

class Section:

    def __init__(self, gui, *args, gns_dir=None, root=None, label=None, gns_file_name=None, **kwargs):
        from arjuna.interact.gui.gom import Section
        label = label and label or self.__class__.__name__
        self.__section = Section(gui, *args, gns_dir=gns_dir, root=root, label=label, gns_file_name=gns_file_name, **kwargs)

    def __getattr__(self, name):
        return getattr(self.__section, name)

Widget = Section
Dialog = Section

class WebApp:

    def __init__(self, *args, base_url=None, blank_slate=False, config=None, ext_config=None, label=None, gns_dir=None, gns_file_name=None, **kwargs):
        from arjuna.interact.gui.gom import WebApp
        label = label and label or self.__class__.__name__
        self.__app = WebApp(*args, base_url=base_url, blank_slate=blank_slate, config=config, ext_config=ext_config, label=label, gns_dir=gns_dir, gns_file_name=gns_file_name, **kwargs)

    def __getattr__(self, name):
        return getattr(self.__app, name)