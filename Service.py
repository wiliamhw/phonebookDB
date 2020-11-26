from flask import Flask,current_app, jsonify, make_response, Response,  Blueprint, abort,render_template, request, redirect,render_template_string, url_for, send_from_directory
from flask_restful import Api, Resource, reqparse,wraps
import uuid
import json
from PhoneBookModel import *

class PhoneBooksAPI(Resource):
    def __init__(self):
        self.phonebook = PhoneBook()
    def get(self):
        s = self.phonebook.list()
        return jsonify(s)
    def post(self):
        self.datakirim = request.json() or dict()
        s = self.phonebook.create(self.datakirim)
        return jsonify(s)

class PhoneBookAPI(Resource):
    def __init__(self):
        self.phonebook = PhoneBook()
    def get(self,id):
        s = self.phonebook.read(id)
        return jsonify(s)
    def put(self,id):
        info = request.json() or dict()
        s = self.phonebook.update(id,info)
        return jsonify(s)
    def delete(self,id):
        s = self.phonebook.delete(id)
        return jsonify(s)


def get_flask(name):
    app = Flask(name)
    app.secret_key = b'781231casda9871293812h3'
    return app

def get_blueprint(nama):
    app = get_flask(__name__)
    api = Api(app)
    api.add_resource(PhoneBooksAPI,'/phones',endpoint='phones')
    api.add_resource(PhoneBookAPI,'/phones/<id>',endpoint='phone')
    return app

app = get_blueprint(__name__)
if __name__=='__main__':
    app.run(host='0.0.0.0', port=32000, debug=True)