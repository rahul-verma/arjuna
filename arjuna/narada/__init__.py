import os
from flask import request, Response
from flask_restful import Resource

MY_DIR = os.path.dirname(os.path.realpath(__file__))
RES_DIR = os.path.join(MY_DIR, "res")

class NaradaSvc(Resource):

    def get(self, path):
        f = open(os.path.join(RES_DIR, path), "r")
        res = f.read().replace("${BODY}", "Hello there")
        return Response(res, mimetype="text/html")
