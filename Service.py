from flask import Flask,current_app, jsonify, make_response, Response,  Blueprint, abort,render_template, request, redirect,render_template_string, url_for, send_from_directory
from flask_restful import Api, Resource, reqparse,wraps
import uuid
import json
from Provisioning import *

class ProvisioningsAPI(Resource):
    def __init__(self):
        self.provisioning = ProvisioningModel()
    def get(self):
        s = self.provisioning.list()
        return jsonify(s)
    def post(self):
        try:
            self.datakirim = request.get_json()
        except:
            self.datakirim=dict()
        s = self.provisioning.create(self.datakirim)
        return jsonify(s)


def get_flask(name):
    app = Flask(name)
    app.secret_key = b'781231casda9871293812h3'
    return app

def get_blueprint(nama):
    app = get_flask(__name__)
    api = Api(app)
    api.add_resource(ProvisioningsAPI,'/pbservices',endpoint='pbservices')
    return app

app = get_blueprint(__name__)
if __name__=='__main__':
    app.run(host='0.0.0.0', port=34000, debug=True)