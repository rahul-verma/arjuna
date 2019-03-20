from flask import Flask, request
from flask_restful import Resource, Api

import os
import sys
import time

def join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

root_dir = os.path.dirname(os.path.realpath(__file__))
importables_dir = join_paths(root_dir, "third_party")

sys.path.insert(0, importables_dir)
sys.path.insert(0, root_dir)

from arjuna.lib.setu.interface.setu import SetuSvc

from arjuna.lib.setu.core.config.processor import ConfigCreator
ConfigCreator.init()

app = Flask(__name__)
api = Api(app)



api.add_resource(SetuSvc, '/setu', endpoint='setu')

# api.add_resource(ItemList, '/items', endpoint='items')
app.run(port=9000, debug=True, use_evalex=False)