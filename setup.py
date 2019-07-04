from setuptools import setup

setup(
    name = "arjuna",
    version = "0.7.1-beta",
    description = "Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net).",
    author = "Rahul Verma",
    author_email = "rv@testmile.com",
    packages = ["arjuna"],
    install_requires = ["flask", "waitress", "requests", "selenium", "xlrd", "xlwt", "pyparsing", "pyhocon"],
    keywords = "arjuna setu unitee selenium testing automation page-object",

)