import sys
import os
from arjuna.main import main

args = sys.argv

if "launch-setu" not in args:
    proj_dir = os.path.dirname(os.path.realpath(__file__))
    args.extend(("-p", proj_dir))
main(args)