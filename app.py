from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
import datetime
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'columbus'
COLLECTION_NAME = 'data'

@app.route("/")
def index():
    return render_template("/index.html")
	
@app.route("/calls/months")
def calls_months():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    data = collection.aggregate([{ "$group": { "_id": {"$substr" : ["$Heure de fin de l'appel",0,7]},"number_of_calls": { "$sum": 1 }}},{ "$sort": { "_id": 1 }}])
    json_data = []
    for datas in data:
        json_data.append(datas)
    json_data = json.dumps(json_data, default=json_util.default)
    connection.close()
    return json_data
	
@app.route("/minutes/months")
def minutes_months():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    data = collection.aggregate([{ "$group": { "_id":{"$substr" : ["$Heure de fin de l'appel",0,7]},"total_time":{ "$addToSet": "$Durée de conversation"}}}])
    json_data = []
    for datas in data:
        sum = datetime.timedelta()
        for i in datas['total_time']:
            if i.count(":") > 0:
                (h, m, s) = i.split(':')
                d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                sum += d
        json_data.append({"month":datas['_id'],"Total_time_Conversation":str(sum)})
    json_data = json.dumps(json_data, default=json_util.default)
    connection.close()
    return json_data	

@app.route("/agent/calls")
def agent_calls():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    data = collection.aggregate([{ "$group": { "_id": "$Nom de l'agent","number_of_calls": { "$sum": 1 }}}])
    json_data = []
    for datas in data:
        json_data.append(datas)
    json_data = json.dumps(json_data, default=json_util.default)
    connection.close()
    return json_data		

@app.route("/agent/months")
def agent_months():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    data = collection.aggregate([{ "$group": { "_id": {"month":{"$substr" : ["$Heure de fin de l'appel",0,7]},"agent":"$Nom de l'agent"},"number_of_calls": { "$sum": 1 }}},{ "$sort": { "_id": 1 }}])
    json_data = []
    for datas in data:
        json_data.append({"month":datas['_id']['month'],datas['_id']['agent']:datas['number_of_calls']})
    json_data = json.dumps(json_data, default=json_util.default)
    connection.close()
    return json_data
	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5010,debug=True)
