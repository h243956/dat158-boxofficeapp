from app import app
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, make_response
import pickle
from app.predict import preprocess, predict, postprocess

app.config['SECRET_KEY'] = 'DAT158'


@app.route('/api')
def Welcome():
    return  "Welcome to the API!!!"

@app.route('/api/test')
def Test():
    status={}
    status["status"]='DONE'
    status["message"]='did my job, boss.'
    return make_response(jsonify(status), 200)


@app.route('/')
def serve():
    return render_template('index.html')
