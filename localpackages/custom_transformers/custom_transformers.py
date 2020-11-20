from sklearn.base import TransformerMixin, BaseEstimator, clone
from collections import Counter
import pandas as pd
import numpy as np
import ast

useless_features = ["imdb_id","original_title","overview","poster_path","tagline","status","title",\
           "spoken_languages","release_date","crew"]

class AddComputedColumns(BaseEstimator, TransformerMixin):

    def transform(self, X, **transform_params):
        trans=HelperFunctions.date_features(self, X)
        trans=HelperFunctions.set_original_language_english(self, trans)
        trans=HelperFunctions.add_crossover_columns(self, trans)
        return trans

    def fit(self, X, y=None, **fit_params):
        return self


class SelectColumnsTransformer(BaseEstimator, TransformerMixin):
    def transform(self, X, **transform_params):
        columns = ["budget", "popularity", "runtime", "release_date", "original_language"]
        trans = X[columns].copy() 
        return trans

    def fit(self, X, y=None, **fit_params):
        return self
    
class DropAllZeroRowsTransformer(BaseEstimator, TransformerMixin):
    def transform(self, X, **transform_params):
        X.replace(0, float("NaN"), inplace=True)
        X.dropna(axis=0, how="any", inplace=True)
        return X

    def fit(self, X, y=None, **fit_params):
        return self
    
class DataFrameFeatureUnion(BaseEstimator, TransformerMixin):
    def __init__(self, list_of_transformers):
        self.list_of_transformers = list_of_transformers
        
    def transform(self, X, **transformparamn):
        concatted = pd.concat([transformer.transform(X)
                            for transformer in
                            self.fitted_transformers_], axis=1).copy()
        return concatted


    def fit(self, X, y=None, **fitparams):
        self.fitted_transformers_ = []
        for transformer in self.list_of_transformers:
            fitted_trans = clone(transformer).fit(X, y=None, **fitparams)
            self.fitted_transformers_.append(fitted_trans)
        return self



class HelperFunctions():
    
    def date_features(self, df):
        df[['release_month','release_day','release_year']]=df['release_date'].str.split('/',expand=True).replace(np.nan, -1).astype(int)
        df.loc[ (df['release_year'] <= 19) & (df['release_year'] < 100), "release_year"] += 2000
        df.loc[ (df['release_year'] > 19)  & (df['release_year'] < 100), "release_year"] += 1900

        releaseDate = pd.to_datetime(df['release_date']) 
        df['release_dayofweek'] = releaseDate.dt.dayofweek
        df['release_quarter'] = releaseDate.dt.quarter
        df=df.drop('release_date', axis=1)
        return df

    def prepare_genres(self, df):
        df['genres'] = df['genres'].apply(lambda x: {} if pd.isna(x) else ast.literal_eval(x))
        df['genres'].apply(lambda x: len(x) if x != {} else 0).value_counts()
        list_of_genres = list(df['genres'].apply(lambda x: [i['name'] for i in x] if x != {} else []).values)
        df['num_genres'] = df['genres'].apply(lambda x: len(x) if x != {} else 0)
        df['all_genres'] = df['genres'].apply(lambda x: ' '.join(sorted([i['name'] for i in x])) if x != {} else '')
        top_genres = [m[0] for m in Counter([i for j in list_of_genres for i in j]).most_common(15)]
        for g in top_genres:
            df['genre_' + g] = df['all_genres'].apply(lambda x: 1 if g in x else 0)

        df = df.drop(['genres'], axis=1)
        df = df.drop(['all_genres'], axis=1)

        return df

    def set_original_language_english(self,df):
        df['isOriginalLanguageEng'] = 0 
        df.loc[ df['original_language'] == "en" ,"isOriginalLanguageEng"] = 1
        df = df.drop(["original_language"], axis=1)
        return df

    def add_crossover_columns(self, df):
        df['budget_popularity_ratio'] = df['budget']/df['popularity']
        df['release_year_popularity_ratio'] = df['release_year']/df['popularity']
        df['release_year_popularity_ratio2'] = df['popularity']/df['release_year']
        return df