import sys
import os

local_arj_path = "/Users/rahulverma/Documents/github_tm/arjuna"
sys.path.insert(0, local_arj_path)

from arjuna.main import main
args = sys.argv
project_dir = os.path.dirname(os.path.realpath(__file__))
args.extend(("-p", project_dir))
main(*args)