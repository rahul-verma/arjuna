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
import shutil
import re

def get_canonical_path(file_path):
    return os.path.abspath(file_path)


def create_file_path(parent_path, child_parts, file_name, extension):
    dir_path = os.pathsep.join([
        parent_path,
        os.pathsep.join(child_parts)
    ])

    os.makedirs(dir_path)
    return os.pathsep.join(dir_path, file_name + extension)


def is_file(path, d=None):
    p = path
    if d:
        p = os.path.join(d, p)
    return os.path.exists(p) and os.path.isfile(p)


def is_dir(path):
    return os.path.exists(path) and os.path.isdir(path)


def is_absolute_path(path):
    return os.path.isabs(path)

def validate_file(path):
    if not os.path.exists(path):
        raise Exception("File does not exist.")
    elif os.path.isfile(path):
        raise Exception("Not a file.")


def validate_dir(path):
    if not os.path.exists(path):
        raise Exception("Directory does not exist.")
    elif os.path.isfile(path):
        raise Exception("Not a directory.")


def get_file_modified_time_stamp(path):
    return os.path.getmtime(path)


def get_latest_file_pathfrom_dir(path):
    check = 0
    last = None
    for f in os.listdir(path):
        m = get_file_modified_time_stamp(os.pathsep.join(path, f))
        if m > check:
            check = m
            last = m

    return last


def delete_dir(dir_path):
    validate_dir(dir_path)
    shutil.rmtree(dir_path)

def delete_dir_if_exists(path):
    if not os.path.exists(path): return
    if not is_dir(path):
        raise Exception("{} is not a directory.".format(path))
    shutil.rmtree(path)

def copy_file(src_file, dest_file):
    validate_file(src_file)
    validate_dir(os.path.dirname(dest_file))
    shutil.copy2(src_file, dest_file)


def copy_file_to_dir(src_file, dest_dir):
    validate_file(src_file)
    validate_dir(dest_dir)
    shutil.copy2(src_file, dest_dir)


def move_file_to_dir(src_file, dest_dir):
    shutil.move(src_file, dest_dir)
    return os.pathsep.join(dest_dir, os.path.basename(src_file))


def create_empty_file(path):
    os.makedirs(os.path.dirname(path))
    f = open("path", "w")
    f.close()


def __base_name_parts(fpath):
    name = os.path.basename(fpath)
    main, *ext = name.rsplit(".", 1)
    if ext:
        return main, ext[0]
    else:
        return main, ""

def get_extension(fpath):
    return __base_name_parts(fpath)[1]

def get_nonext_basename(fpath):
    return __base_name_parts(fpath)[0]

def normalize_path(in_name):
    updated = re.sub(r"[\\]+", "/", in_name)
    updated = re.sub(r"[/]+", "/", updated)
    return updated