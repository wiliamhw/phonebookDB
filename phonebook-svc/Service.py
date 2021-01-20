from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from PhoneBookModelRedis import *
import os
#menggunakan PhoneBookModelRedis, untuk implementasi menggunakan redis kv store
#service layer dari phonebook db tetap seperti biasa



class PhoneBooksAPI(Resource):
    def __init__(self):
        self.phonebook = PhoneBook()
    def get(self):
        s = self.phonebook.list()
        return jsonify(s)
    def post(self):
        try:
            self.datakirim = request.get_json()
        except:
            self.datakirim=dict()
        s = self.phonebook.create(self.datakirim)
        return jsonify(s)

class PhoneBookAPI(Resource):
    def __init__(self):
        self.phonebook = PhoneBook()
    def get(self,id):
        s = self.phonebook.read(id)
        return jsonify(s)
    def put(self,id):
        try:
            info = request.get_json()
        except:
            info = dict()
        s = self.phonebook.update(id,info)
        return jsonify(s)
    def delete(self,id):
        s = self.phonebook.delete(id)
        return jsonify(s)


def get_flask(name):
    app = Flask(name)
    app.secret_key = b'781231casda9871293812h3'
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    return app

def get_blueprint(nama):
    app = get_flask(__name__)
    api = Api(app)
    api.add_resource(PhoneBooksAPI,'/phones',endpoint='phones')
    api.add_resource(PhoneBookAPI,'/phones/<id>',endpoint='phone')
    return app

app = get_blueprint(__name__)


#dipindah ke wsgi.py
if __name__=='__main__':
    #setup environment, untuk proses debuggind di pycharm
    os.environ['REDIS_SERVER']='172.25.0.2'
    app.run(host='0.0.0.0', port=32006, debug=True)
#jika dijalankan dari pycharm, port yang digunakan adalah 32006, dan dapat diakses menggunakan localhost
#ip dari redis-server dapat diketahui dari (docker inspect redis-server | grep "IPAddress")
#jika dijalankan dari gunicorn, port yang digunakan adalah 32000 (lihat di script start.sh)