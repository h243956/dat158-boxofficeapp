from sklearn.base import TransformerMixin, BaseEstimator, clone
import pandas as pd

class SelectColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=[]):
        self.columns = columns

    def transform(self, X, **transform_params):
        trans = X[self.columns].copy() 
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