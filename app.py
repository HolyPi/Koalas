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
    r = requests.get('https://some-random-api.ml/img/koala')
    p = requests.get('https://some-random-api.ml/facts/koala')

    if r.status_code == 200:
        koala = json.loads(r.content)['link']
        koalaf = json.loads(p.content)['fact']

    else:
        koala = None
        koalaf = None

    return render_template('index.html', koala = koala, koalaf = koalaf)
