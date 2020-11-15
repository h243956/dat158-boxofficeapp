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
    genre = SelectField("Sjangrar", validators=[required()], choices=genres.genres)
    budget = IntegerField("Budsjett", validators=[required()])
    popularity = FloatField("Popularitet", validators=[required()])

    submit = SubmitField('Submit')

