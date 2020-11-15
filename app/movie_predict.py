import numpy as np
import pandas as pd
import joblib

####### 
## Get the model trained in the notebook 
# `../nbs/1.0-asl-train_model.ipynb`
#######

model = joblib.load('models/boxoffice_model.joblib')
pipeline = joblib.load('models/transform_predict.joblib') 


def preprocess(data):
    """
    Returns the features entered by the user in the web form. 

    To simplify, we set a bunch of default values. 
            For bools and ints, use the most frequent value
            For floats, use the median value

    Note that this represent some major assumptions that you'd 
    not want to make in real life. If you want to use default 
    values for some features then you'll have to think more 
    carefully about what they should be. 

    F.ex. if the user doesn't provide a value for BMI, 
    then one could use a value that makes more sense than 
    below. For example, the mean for the given gender would 
    at least be a bit more correct. 
    
    Having _dynamic defaults_ is important. And of course, if 
    relevant, getting some of the features without asking the user. 
    E.g. if the user is logged in and you can pull information 
    form a user profile. Or if you can compute or obtain the information 
    thorugh other means (e.g. user location if shared etc).
    """


    feature_values = {
        'id': None,
        'belongs_to_collection': None,
        'budget': 5555555,
        'genres': [{'id': 12, 'name': 'Adventure'}],
        'homepage': None,
        'imdb_id': "tt0051380",
        'original_language': "en",
        'original_title': "kaka",
        'overview': "adssada",
        'popularity': 0.0,
        'poster_path': "dasdsa",
        'production_companies': None,
        'production_countries': None,
        'release_date': 2020,
        'runtime': None,
        'spoken_languages': [{'iso_639_1': 'en', 'name': 'English'}],
        'status': "Released",
        'tagline': None,
        'title': None,
        'Keywords': None,
        'cast': None,
        'crew': None
    }


    # Parse the form inputs and return the defaults updated with values entered.

    for key in [k for k in data.keys() if k in feature_values.keys()]:
        feature_values[key] = data[key]

    return feature_values



####### 
## Now we can predict with the trained model:
#######


def predict(data):
    """
    If debug, print various useful info to the terminal.
    """
 
    # Store the data in an array in the correct order:

    column_order = ['id', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'imdb_id', 
                    'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 
                    'production_companies', 'production_countries', 'release_date', 'runtime', 'spoken_languages', 
                    'status', 'tagline', 'title', 'Keywords', 'cast', 'crew']

    data = np.array([data[feature] for feature in column_order], dtype=object)

    ## TODO work out preprocessiong of data before predicting
    ## how data looks
    #[None None 2121 list([{'id': 12, 'name': 'Adventure'}]) None 'tt0051380' 'en' 'kaka' 'adssada' 12.0 'dasdsa' None None 2020 None list([{'iso_639_1': 'en', 'name': 'English'}]) 'Released' None None None None None]


    # NB: In this case we didn't do any preprocessing of the data before 
    # training our random forest model (see the notebool `nbs/1.0-asl-train_model.ipynb`). 
    # If you plan to feed the training data through a preprocessing pipeline in your 
    # own work, make sure you do the same to the data entered by the user before 
    # predicting with the trained model. This can be achieved by saving an entire 
    # sckikit-learn pipeline, for example using joblib as in the notebook.
    
    #transformed_data = pipeline.transform(data)

    
    #pred = model.predict(transformed_data.reshape(1,-1))

    #uncertainty = model.predict_proba(transformed_data.reshape(1,-1))

    return data


def postprocess(prediction):
    """
    Apply postprocessing to the prediction. E.g. validate the output value, add
    additional information etc. 
    """

    pred, uncertainty = prediction

    # Validate. As an example, if the output is an int, check that it is positive.
    try: 
        int(pred[0]) > 0
    except:
        pass

    # Make strings
    pred = str(pred[0])
    uncertainty = str(uncertainty[0])


    # Return
    return_dict = {'pred': pred, 'uncertainty': uncertainty}

    return return_dict