from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SelectMultipleField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, required
import tmdbsimple as tmdb

class MovieForm(FlaskForm):

    #choices=[]
    #for genre in genres.genres:
    #    choices.insert(genre['id'], genre['name'])
    genres = tmdb.Genres()
    genres.movie_list()
    #genres = SelectField("Sjangrar", validators=[required()], choices=genres.genres)
    budget = IntegerField("Budsjett [i USD, 0-380 000 000]", validators=[required()])
    popularity = FloatField("Popularitet [0.0-300.0]", validators=[required()])
    runtime = IntegerField("Filmlengde [i minutt]", validators=[required()])
    release_date = StringField("Gitt ut dato [mm/dd/yy]", validators=[required()])
    original_language = StringField("Orginalt språk [en]", validators=[required()])

    submit = SubmitField('Submit')

