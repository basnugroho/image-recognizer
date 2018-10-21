from flask import Flask, jsonify, requests
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db['Users']

def UserExist(username):
    if users.find({"Username": username}).count()==0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = requests.get_json()

        username = postedData['username']
        password = postedData['password']

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "username already exist!"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashed_pw(password.encode("utf8"), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 4
        })

        retJson = {
            "status": 200,
            "msg": "you succesfully sign up via this API"
        }
        return jsonify(retJson)
