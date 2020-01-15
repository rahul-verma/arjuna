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

import os
import sys
import platform

def is_os_windows():
    return platform.system() == "Windows"

def cexit():
	from arjuna.tpi import Arjuna
	Arjuna.get_console().display_error("Exiting...")
	sys.exit()

def fexit():
	print("Exiting because of Fatal Error...", file=sys.stderr)
	import time
	time.sleep(0.5)
	sys.exit(1)

# public static Runtime get_run_time() {
#     return Runtime.get_runtime();
# }

# public static String getOSName() {
#     return System.get_property("os.name");
# }

def get_line_separator():
    return os.linesep


def get_path_separator():
    return os.sep
