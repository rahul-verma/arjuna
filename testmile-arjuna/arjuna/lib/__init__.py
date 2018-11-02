'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

import time
from arjuna.lib.core.reader.textfile import TextResourceReader
from arjuna.lib.interface.cli import ArjunaCLI

class __arfacade():

    def __init__(self):
        self.__version = "0.6.5-beta"

    def launch(self, raw_args):
        reader = TextResourceReader("header.txt")
        print(reader.read().format(version=self.__version))
        reader.close()

        cli = ArjunaCLI(raw_args)
        # Initialize the Arjuna Core as per CLI options
        cli.init()

        cli.execute()

Arjuna = __arfacade()

from arjuna.lib.unitee.markup import tsmarkup

markup = tsmarkup