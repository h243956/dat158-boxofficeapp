import numpy as np
import pandas as pd
import joblib

model = joblib.load('models/boxoffice_model.joblib')
pipeline = joblib.load('models/transform_predict.joblib') 

def preprocess(data):

    feature_values = {
        'id': None,
        'belongs_to_collection': None,
        'budget': 5555555,
        'genres': [{'id': 35, 'name': 'Comedy'}, {'id': 18, 'name': 'Drama'}, {'id': 10751, 'name': 'Family'}, {'id': 10749, 'name': 'Romance'}],
        'homepage': "sadsadadadsa",
        'imdb_id': "tt0051380",
        'original_language': "en",
        'original_title': "kaka",
        'overview': "adssada",
        'popularity': 12,
        'poster_path': "dasdsa",
        'production_companies': [{'name': 'Paramount Pictures', 'id': 4}, {'name': 'United Artists', 'id': 60}, {'name': 'Metro-Goldwyn-Mayer (MGM)', 'id': 8411}],
        'production_countries': None,
        'release_date': "2/20/15",
        'runtime': 122,
        'spoken_languages': [{'iso_639_1': 'en', 'name': 'English'}],
        'status': "Released",
        'tagline': None,
        'title': None,
        'Keywords': [{'id': 4379, 'name': 'time travel'}, {'id': 9663, 'name': 'sequel'}, {'id': 11830, 'name': 'hot tub'}, {'id': 179431, 'name': 'duringcreditsstinger'}],
        'cast': None,
        'crew': None
    }


    # Parse the form inputs and return the defaults updated with values entered.
    for key in [k for k in data.keys() if k in feature_values.keys()]:
        feature_values[key] = data[key]

    return feature_values





def predict(data):

    column_order = ['id', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'imdb_id', 
                    'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 
                    'production_companies', 'production_countries', 'release_date', 'runtime', 'spoken_languages', 
                    'status', 'tagline', 'title', 'Keywords', 'cast', 'crew']

    data = np.array([data[feature] for feature in column_order], dtype=object)
    data = pd.DataFrame(data=[data], index=["first"], columns=column_order)

    transformed_data = pipeline.transform(data)
    pred = model.predict(transformed_data.reshape(1,-1))
    return pred


def postprocess(prediction):
    prediction = "Prediction: " + str(prediction[0])
    return prediction