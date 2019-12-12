from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import os
from bson.objectid import ObjectId
import requests

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Koalas')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
koalas = db.koalas


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', koalas=koalas.find())

@app.route('/koalas/new')
def koalas_new():
    """Create a new koala form."""
    return render_template('new_koala.html', koala={}, title='New Koala')


@app.route('/koalas/<koala_id>')
def koalas_show(koala_id):
    """Show a Koala."""
    koala = koalas.find_one({'_id': ObjectId(koala_id)})
    return render_template('koala_show.html', koala=koala)


@app.route('/home', methods=['GET','POST'])
def home():
    r = requests.get('https://some-random-api.ml/img/koala')
    p = requests.get('https://some-random-api.ml/facts/koala')

    if r.status_code == 200:
        koala = json.loads(r.content)['link']
        koalaf = json.loads(p.content)['fact']

    else:
        koala = None
        koalaf = None

    return render_template('home.html', koala = koala, koalaf = koalaf)

@app.route('/koalas/<koala_id>/edit')
def koalas_edit(koala_id):
    """Show the edit form for the koalas."""
    koala = koalas.find_one({'_id': ObjectId(koala_id)})
    return render_template('koalas_edit.html', koala=koala, title="Edit Koala") 



@app.route('/koalas/<koala_id>', methods=['POST'])
def koala_update(koala_id):
    """Submit an edited koala."""
    update_koala = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'url': request.form.get('url'),
    }
    koalas.update_one(
        {'_id': ObjectId(koala_id)},
        {'$set': update_koala})
    return redirect(url_for('koalas_show', koala_id=koala_id))

@app.route('/koalas', methods=['POST'])
def submit_koala():
    koala = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'url': request.form.get('url')
    }
    koala_id = koalas.insert_one(koala).inserted_id
    return redirect(url_for('koalas_show', koala_id=koala_id))


@app.route('/koalas/<koala_id>/delete', methods=['POST'])
def koala_delete(koala_id):
    """Deletes a koala."""
    koalas.delete_one({'_id': ObjectId(koala_id)})
    return redirect(url_for('index'))