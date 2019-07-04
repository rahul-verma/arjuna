from setuptools import setup

setup(
    name = "arjuna",
    version = "0.7.1",
    url = "https://testmile.com/arjuna",
    description = "Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net).",
    author = "Rahul Verma",
    author_email = "rv@testmile.com",
    packages = ["arjuna"],
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