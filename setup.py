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

import os
from setuptools import setup, find_packages

packages = find_packages()

this_directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "arjuna",
    version = "1.1.7",
    url = "https://rahulverma.net",
    description = "Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net).",
    author = "Rahul Verma",
    author_email = "",
    packages = packages,
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data = {
        '' :  [
                    "*.txt",
                    "*.md",
                    "*.cfg",
        ],
        'arjuna' : [
                    "res/*.xml",
                    "res/*.help",
                    "res/*.txt",
                    "res/*.conf",
                    "res/*.ini",
                    "res/*.py",
                    "res/*.yaml",
                    "res/*.css",
                    "res/*.js",
                    "res/*.html"
                ]
    },
    install_requires = ["lxml", "requests", "requests-toolbelt", "selenium", "webdriver_manager", "xlrd", "xlwt", "pyparsing", "pyhocon", "pytest", "pytest-html", "pytest-dependency", "PyYAML", "mimesis", "jsonpath-rw", "jsonpath-rw-ext", "genson", "jsonschema", "Pallets-Sphinx-Themes", "oauthlib", "requests_oauthlib", "bs4", "browsermob-proxy", "haralyzer"],
    keywords = "arjuna selenium testing automation page-object data-driven",
    license = "Apache License, Version 2.0",
    classifiers=[
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: OS Independent',
    'Natural Language :: English'
    ]
)
