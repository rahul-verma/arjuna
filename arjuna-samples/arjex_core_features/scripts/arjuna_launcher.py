import sys
import os

from arjuna.main import main
args = sys.argv
project_dir = os.path.dirname(os.path.realpath(__file__))
args.extend(("-p", project_dir))
main(*args)