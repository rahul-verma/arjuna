from flask import Flask
from flask_restful import Api


def launch_setu(port):
    from arjuna.lib.setu.interface.setu import SetuSvc

    from arjuna.lib.setu.core.config.processor import ConfigCreator
    ConfigCreator.init()

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(SetuSvc, '/setu', endpoint='setu')

    # api.add_resource(ItemList, '/items', endpoint='items')
    app.run(port=port, use_evalex=False) #, debug=True)