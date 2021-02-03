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

"""
Arjuna

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses **[pytest](https://docs.pytest.org/en/latest/)** as its recommended test engine. Arjuna also provides its markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

To import all public names for test automation authors with
from arjuna import *

To run arjuna as a module

    $python -m arjuna <options>

To see which command line options are available:

    $python -m arjuna -h

All classes, functions and names supposed to be used in test automation code are available in Tester Programming Interface: **arjuna.tpi** package.
"""

import pkg_resources
import time
import os
import sys

def __join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

__root_dir = __join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
__importables_dir = __join_paths(__root_dir, "third_party")

sys.path.insert(0, __importables_dir)
sys.path.insert(0, __root_dir)

class _ArjunFacade:

    def __init__(self):
        self.__version = pkg_resources.require("arjuna")[0].version

    def load(self, raw_args):
        from arjuna.tpi.parser.text import _TextResource
        from arjuna.interface.cli import ArjunaCLI
        reader = _TextResource("header.txt")
        print(reader.read().format(version=self.__version))
        reader.close()

        print("Parsing CLI Options...")
        cli = ArjunaCLI(raw_args)
        # Initialize the Arjuna Core as per CLI options
        print("Intializing Arjuna...")
        cli.init()

        print("Loading Arjuna core to allow third party test engine to take over test execution...")
        cli.load()

    def launch(self, raw_args):
        from arjuna.tpi.parser.text import _TextResource
        from arjuna.interface.cli import ArjunaCLI
        reader = _TextResource("header.txt")
        print(reader.read().format(version=self.__version))
        reader.close()

        print("Parsing CLI Options...")
        cli = ArjunaCLI(raw_args)
        # Initialize the Arjuna Core as per CLI options
        print("Intializing Arjuna...")
        cli.init()

        print("Executing Arjuna Command...")
        cli.execute()

from arjuna.tpi.engine import Arjuna

from arjuna.tpi.error import *
from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.tpi.tracker import track
from arjuna.tpi.helper.arjtype import nvpair, nvpairs, withx, Screen, attr, node, bnode, fnode, Point, Offset, NetworkPacketInfo, oneof, axes
from arjuna.tpi.helper.extract import pos
from arjuna.tpi.helper.audit import HardCoded
from arjuna.tpi.helper.arjtype import ProcessedKeyDict
from arjuna.tpi.helper.datetime import Time, DateTime, DateTimeDelta, DateTimeStepper

from arjuna.tpi.parser.json import Json, JsonSchema
from arjuna.tpi.parser.xml import Xml
from arjuna.tpi.parser.html import Html
from arjuna.tpi.parser.text import Text

from arjuna.tpi.engine.test import *
from arjuna.tpi.engine.relation import *
from arjuna.tpi.engine.resource import *
from arjuna.tpi.engine.data_markup import *

from arjuna.tpi.error import *

from arjuna.tpi.data.record import *
from arjuna.tpi.data.generator import Random, Locales, generator, composite, composer
from arjuna.tpi.data.entity import data_entity

from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition
gui_widget_def = GuiWidgetDefinition
widget = GuiWidgetDefinition
from arjuna.tpi.guiauto.model.app import GuiApp
from arjuna.tpi.guiauto.model.page import GuiPage
from arjuna.tpi.guiauto.model.section import GuiSection
from arjuna.tpi.guiauto.model.dialog import GuiDialog
from arjuna.tpi.guiauto.helper import Keys

from arjuna.tpi.httpauto.http import Http
from arjuna.tpi.httpauto.oauth import OAuthImplicitGrantSession

from arjuna.tpi.dbauto.db import DB

from arjuna.tpi.hook.config import Configurator

from arjuna.tpi.log import *
from arjuna.tpi.magic import C, L, R
