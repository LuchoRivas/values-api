import pymongo
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime
from constants import MONGO_URI

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)


@app.route('/')
def index():
    date_now = datetime.now()
    dt_string = date_now.strftime("%d/%m/%Y %H:%M:%S")

    return "<h3>🙇‍♂️ " + dt_string + "</h3>"


@app.route('/values', methods=['GET'])
def get_values():
    values = mongo.db.values.find_one({}, {'_id': 0, 'creationDate': 0}, sort=[
                                      ('_id', pymongo.DESCENDING)])
    response = json_util.dumps(values)

    return Response(response, mimetype="application/json")


@app.route('/types', methods=['GET'])
def get_types():
    types = mongo.db.types.find({})
    response = json_util.dumps(types)

    return Response(response, mimetype="application/json")


# esto no corre con el debugger
# cambiar a 0.0.0.0 Debug=True para local
if __name__ == "__main__":
    app.run(threaded=True, port=5000)
