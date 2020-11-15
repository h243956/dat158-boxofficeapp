from app import app
from flask import render_template, session, redirect, url_for, request
import pickle
import tmdbsimple as tmdb
tmdb.API_KEY = '591d13f0a8ae82528cbfbc670dd4685d'

import sys

from app.forms import DataForm
from app.movieform import MovieForm
from app.movie_predict import preprocess, predict, postprocess


app.config['SECRET_KEY'] = 'DAT158'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    """
    We grab the form defined in `forms.py`. 
    If the form is submitted (and passes the validators) 
    then we grab all the values entered by the user and 
    predict. 
    """


    # Handle request from form
    #form = DataForm()
    #if form.validate_on_submit():

        # If the form is submitted and validated, store all the 
        # inputs in session
       # for fieldname, value in form.data.items():
       #     session[fieldname] = value


        # Get additional user data
      #  user_info = request.headers.get('User-Agent')

        # Preprocess data
       # data = preprocess(session)

        # Get model outputs 
       # pred = predict(data)

        # Postprocess results
      #  pred = postprocess(pred)

        # Create the payload (we use session)
      #  session['user_info'] = user_info
      #  session['pred'] = pred


    return render_template('index.html')



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/movie', methods=['GET', 'POST'])
def movie():
    data=None
    form = MovieForm()
    
    if form.validate_on_submit():
        for fieldname, value in form.data.items():
            session[fieldname] = value

        
        data = preprocess(session)
        data = predict(data)
        #data = postprocess(data)
            
        return render_template('test.html', data=data)

    return render_template('movieform.html', form=form, data=data)

@app.route('/test')
def test():
    genres = tmdb.Genres()
    genres.movie_list()

    data=[]
    for genre in genres.genres:
        data.insert(genre['id'], genre['name'])

    return render_template('test.html', data=data)

    

    
