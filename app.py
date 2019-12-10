from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import requests

#foxinfo = db.foxinfo


app = Flask(__name__)

#client = MongoClient()
#db = client.get_default_database()


@app.route('/', methods=['GET','POST'])
def index():
    r = requests.get('https://some-random-api.ml/img/red_panda')

    if r.status_code == 200:
        rpanda = json.loads(r.content)['link']
    else:
        rpanda = ""

    return render_template('index.html', rpanda = rpanda)
