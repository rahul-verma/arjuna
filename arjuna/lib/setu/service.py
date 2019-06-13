from flask import Flask
from flask_restful import Api
from waitress import serve

import time

def __launch_setu_svc(port):
    from arjuna.lib.setu.interface.setu import SetuSvc

    from arjuna.lib.setu.core.config.processor import ConfigCreator
    ConfigCreator.init()

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(SetuSvc, '/setu', endpoint='setu')

    # api.add_resource(ItemList, '/items', endpoint='items')
    #app.run(port=port, use_evalex=False) #, debug=True)
    serve(app, host="localhost", port=port, _quiet=True)

def wait_for_port(port):
    import socket
    server_address = ('localhost', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ct = time.time()
    while(time.time() - ct < 60):
        try:
            sock.bind(server_address)
            sock.close()
            return
        except:
            time.sleep(1)
    print("Port is not open")
    raise RuntimeError("SET_SVC_ERROR:: Another service is running at port {}. Setu could not be launched. Message: ".format(port))

def launch_setu(port):
    from arjuna.lib.setu.core.requester.connector import _DefaultSetuRequester, _DefaultSetuRequest 
    from arjuna.lib.setu.core.requester.action import SetuActionType
    from arjuna.lib.setu.core.requester.config import ArjunaComponent
    requester = _DefaultSetuRequester()
    request = _DefaultSetuRequest(ArjunaComponent.SETU, SetuActionType.HELLO)
    response = None
    try:
        response = requester.post(request)
    except:
        wait_for_port(port)
        print("Port is open")
        __launch_setu_svc(port)   
    else:
        rstring = response.get_value().as_string()
        if rstring.lower().find("hello") == -1:
            raise RuntimeError("SET_SVC_ERROR:: Unexpected Setu error for Hello. Got response: " + rstring)