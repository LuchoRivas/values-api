import pymongo
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://luigi:Luigi2020@cluster0.o2pfg.mongodb.net/db?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    return "<spam>Welcome to our server !!</spam>"

@app.route('/values', methods=['GET'])
def get_values():
    values = mongo.db.values.find_one({}, {'_id': 0, 'creationDate': 0}, sort=[( '_id', pymongo.DESCENDING )])
    response = json_util.dumps(values)
    
    return Response(response, mimetype="application/json")

@app.route('/types', methods=['GET'])
def get_types():
    types = mongo.db.types.find({})
    response = json_util.dumps(types)
    
    return Response(response, mimetype="application/json")

# esto no corre con el debugger
if __name__ == "__main__":
    app.run(threaded=True, port=5000)