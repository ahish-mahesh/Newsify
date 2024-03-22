import flask
from flask import request, jsonify
import sqlite3
from flask_cors import CORS
import json 
import pymongo

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant News Archive</h1>
            <p>A prototype API for distant news.</p>'''


# @app.route('/newsify/users/all', methods=['GET'])
# def api_all():
#     conn = sqlite3.connect('newsifyDb.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     all_users = cur.execute('SELECT * FROM USERS;').fetchall()

#     return jsonify(all_users)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/newsify/sources', methods=['GET'])
def getSources():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    newsifyDb = myclient["newsify"]
    sources = newsifyDb["sources"]

    queryResult = sources.find({}, {"_id": 0, "id": 1, "name": 1})

    sources = []
    for x in queryResult:
        x["text"] = x.pop("name")
        sources.append(x)
    
    return jsonify({'result': sources})

@app.route('/newsify/users', methods=['GET'])
def getUser():
    query_parameters = request.args

    username = query_parameters.get('username')
    password = query_parameters.get('password')


    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["newsify"]
    users = mydb["users"]

    query = {"username": username, "password" : password}
    result = users.find(query)

    for eachDoc in result:
        del eachDoc["_id"]
        return jsonify({'result': eachDoc})
    return jsonify({'result': "Invalid"})

@app.route('/newsify/users', methods=['POST'])
def createUser():
    query_parameters = request.json

    username = query_parameters['username']
    password = query_parameters['password']
    country = query_parameters['country']
    tags = query_parameters['tags']
    sources = query_parameters['sources']

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["newsify"]
    users = mydb["users"]

    if len(list(users.find({"username": username}))) > 0:
        return jsonify({'result': "Exists"})

    entry = {
        "username": username,
        "password": password,
        "country": country,
        "tags": tags,
        "sources": sources,
    }
    

    result = users.insert_one(entry)

    return jsonify({'result': "Success!"})

@app.route('/newsify/users', methods=['PUT'])
def editUser():
    query_parameters = request.json

    username = query_parameters['username']
    password = query_parameters['password']
    country = query_parameters['country']
    tags = query_parameters['tags']
    sources = query_parameters['sources']
    

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["newsify"]
    users = mydb["users"]
    
    query = { "username" : username}

    newValues = {
        "$set" : {
            "password": password,
            "country": country,
            "tags": tags,
            "sources": sources,
        }
    }
    

    result = users.update_one(query, newValues)

    return jsonify({'result': "Success!"})

app.run()
