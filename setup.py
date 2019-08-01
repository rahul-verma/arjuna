import os
from setuptools import setup, find_packages

# my_dir =  os.path.dirname(os.path.realpath(__file__))

# dynamic_dirs = [
#     os.path.join(my_dir, "arjuna", p) for p in (
#         "res",
#         "third_party"
#     )
# ]

packages = find_packages()
# packages.extend(dynamic_dirs)

# print(packages)

this_directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "arjuna",
    version = "0.7.6",
    url = "https://testmile.com/arjuna",
    description = "Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net).",
    author = "Rahul Verma",
    author_email = "rv@testmile.com",
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
                    "res/st/*.xml", 
                    "res/*.help", 
                    "res/*.txt", 
                    "res/scripts/arjuna_launcher.py",
                    "setu/config/res/*.conf", 
                    "setu/config/res/*.txt"
                ]
    },
    install_requires = ["flask", "flask-RESTful", "waitress", "requests", "selenium", "xlrd", "xlwt", "pyparsing", "pyhocon"],
    keywords = "arjuna setu unitee selenium testing automation page-object",
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