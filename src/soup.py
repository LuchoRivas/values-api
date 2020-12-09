from bs4 import BeautifulSoup
import requests
import time
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

client = pymongo.MongoClient(
    "MONGODB_CONNECTION_STR")

collection = client.db.values
query = {"creationDate": {"$lt": datetime.now()}}
sortByDate = [{"creationDate", -1}]


def __eq__(self, other):
    return ((self["blue"], other["blue"]) == (self["oficial"], other["oficial"]))


def getValues():
    url = "https://www.dolarhoy.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    prices = soup.find_all('span', class_='price')
    precio_compra_oficial = prices[0].text
    precio_venta_oficial = prices[1].text
    precio_compra_blue = prices[2].text
    precio_venta_blue = prices[3].text
    precio_compra_bolsa = prices[4].text
    precio_venta_bolsa = prices[5].text
    precio_compra_liqui = prices[6].text
    precio_venta_liqui = prices[7].text

    # Guardar bien / crear relacion con types
    newValues = {
        "oficial": {
            "buy": precio_compra_oficial.strip(),
            "sell": precio_venta_oficial,
            "date": datetime.now()
        },
        "blue": {
            "buy": precio_compra_blue,
            "sell": precio_venta_blue,
            "date": datetime.now()
        },
        "bolsa": {
            "buy": precio_compra_bolsa,
            "sell": precio_venta_bolsa,
            "date": datetime.now()
        },
        "liqui": {
            "buy": precio_compra_liqui,
            "sell": precio_venta_liqui,
            "date": datetime.now()
        },
        "creationDate": datetime.now()
    }

    dbValues = getDbValues()

    if(dbValues == None):
        saveValues(newValues)
    else:
        if(__eq__(dbValues, newValues)):
            return
        else:
            saveValues(newValues)


def saveValues(values):
    try:
        collection.insert_one(values)
        print(f'inserted values!')

    except Exception as e:
        print('an error occurred trying to save values >>', e)


def getDbValues():
    try:
        cursor = collection.find_one({}, sort=[('_id', pymongo.DESCENDING)])
        return cursor

    except Exception as e:
        print('an error occurred trying get values from db >>', e)


def execute():
    getValues()
    time.sleep(60)


while True:
    execute()
