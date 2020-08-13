import time
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config[
    "MONGO_URI"
] = "mongodb://bobjoe:abc@cluster0-shard-00-00.j9y1e.mongodb.net:27017,cluster0-shard-00-01.j9y1e.mongodb.net:27017,cluster0-shard-00-02.j9y1e.mongodb.net:27017/mmr?ssl=true&replicaSet=atlas-k6mnw1-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)

people = [
    "aaron",
    "cam",
    "erik",
    "ian",
    "liam",
    "nicky",
    "vevey",
    "will",
    "yuuki",
    "steve",
]


@app.route("/get_mmr")
@cross_origin()
def get_mmr():
    aaron = mongo.db["aaron"].find()
    response = {}
    for person in people:
        mmr = mongo.db[person].find()
        res_list = []
        for doc in mmr:
            info = {}
            info["mmr"] = doc["mmr"]
            info["id"] = str(doc["_id"])
            res_list.append(info)
        response[person] = res_list

    print(response)
    return response
