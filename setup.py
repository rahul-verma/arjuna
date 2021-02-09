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
from setuptools import setup, find_packages

packages = find_packages()

this_directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "arjuna",
    version = "1.1.37",
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
    install_requires = [
        "pyOpenSSL>=0.14",
        "urllib3==1.25.3",
        "requests==2.22.0",
        "lxml==4.4.1",
        "requests-toolbelt==0.9.1", 
        "selenium==4.0.0a7", 
        "webdriver_manager==3.2.2", 
        "xlrd==1.2.0", 
        "xlwt==1.3.0", 
        "pyparsing==2.4.0", 
        "pyhocon==0.3.51", 
        "pytest==6.2.1", 
        "pytest-html==2.1.1", 
        "pytest-dependency==0.4.0", 
        "PyYAML==5.3", 
        "mimesis==4.0.0", 
        "jsonpath-rw==1.4.0", 
        "jsonpath-rw-ext==1.2.2", 
        "genson==1.2.1", 
        "jsonschema==3.2.0", 
        "Pallets-Sphinx-Themes", 
        "oauthlib==3.1.0", 
        "requests_oauthlib==1.3.0", 
        "bs4==0.0.1", 
        "browsermob-proxy==0.8.0", 
        "haralyzer==1.8.0", 
        "mysql-connector-python==8.0.21"
    ],
    entry_points={"pytest11": ["arjuna = arjuna.engine.pytestplug"]},
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
