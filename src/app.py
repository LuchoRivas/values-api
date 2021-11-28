import pymongo
from flask import Flask, Response
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime
from constants import MONGO_URI, CREATION_DATE, DEFAULT_TYPE

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI


mongo = PyMongo(app)


@app.route('/')
def index():
    date_now = datetime.now()
    dt_string = date_now.strftime("%d/%m/%Y %H:%M:%S")

    return "<h3>🙇‍♂️ " + dt_string + "</h3>"

# Ruta base que obtiene el ultimo registro obtenido por soup
@app.route('/values', methods=['GET'])
def get_values():
    values = mongo.db.values.find_one({}, {'_id': 0, CREATION_DATE: 0}, sort=[
                                      ('_id', pymongo.DESCENDING)])
    response = json_util.dumps(values)

    return Response(response, mimetype="application/json")

# Ruta para obtener los tipos de cotizacion estos poseen un id importante para natchear valor / cotizacion
@app.route('/types', methods=['GET'])
def get_types():
    types = mongo.db.types.find({})
    response = json_util.dumps(types)

    return Response(response, mimetype="application/json")


# WIP: Para obtener datos y poder graficarlos en la app
# deberia retornar solo lo necesario, el obj de la cotizacion elegida (blue x defecto)
# oficial, blue, bolsa, liqui, solidario deberian ser los parametros que la app tiene que enviar aca
# tambien deberia poder recibir el rango de fechas deseado, x ahora se limitara a un par de opciones
@app.route('/chart', methods=['GET'])
def get_chart():
    # convert your date string to datetime object
    start = datetime(2021, 10, 1, 00, 00, 00)
    end = datetime(2021, 10, 10, 00, 00, 00)
    filtro = {DEFAULT_TYPE: 1, '_id': 0}
    query = {CREATION_DATE: {'$lt': end, '$gte': start}}
    result = mongo.db.values.find(query, filtro)
    response = json_util.dumps(result)

    return Response(response, mimetype="application/json")


# esto no corre con el debugger
# cambiar a 0.0.0.0 Debug=True para local
if __name__ == "__main__":
    app.run(threaded=True, port=5000, Debug=True)
