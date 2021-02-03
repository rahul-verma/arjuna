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

import subprocess


def execute_windows_process(proc_name, arg_list=[]):
    '''
    Executes a windows process using the command shell in termination mode.

    Arguments:
    proc_name: Name of process
    arg_list: (Optional) A list of strings that are to be passed as command line arguments to said process.
    '''
    p = subprocess.Popen(
        ["cmd.exe", "/C", proc_name] + arg_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = p.communicate()

    return p.returncode, stdout, stderr


def kill_process(process_name):
    returncode, stdout, stderr = execute_windows_process("taskkill", ["/F", "/IM", process_name])
    if returncode != 0:
        raise Exception("Not able to kill process: " + process_name)


def start_service(name):
    returncode, stdout, stderr = execute_windows_process("sc", ["start", '"%s"'.format(name)])
    if returncode != 0 or not is_service_running(name):
        raise Exception("Unable to start service: " + name)


def stop_service(name):
    returncode, stdout, stderr = execute_windows_process("sc", ["stop", '"%s"'.format(name)])
    if returncode != 0 or is_service_running(name):
        raise Exception("Unable to stop service: " + name)


def is_service_running(name):
    returncode, stdout, stderr = execute_windows_process("sc", ["query", '"%s"'.format(name)])
    if returncode != 0:
        raise Exception("Not able to query service: " + name)
    else:
        return "RUNNING" in stdout
