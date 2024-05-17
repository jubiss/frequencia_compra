import sys,os
sys.path.append(os.getcwd())
from sklearn.base import BaseEstimator, TransformerMixin
from src.features import pre_processing as pp
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

def features_pipeline():
    enc = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    transform_categorical = ColumnTransformer(
        transformers=[
            ('OneHotEncoder', enc, ['bairro']),
        ],
        remainder='passthrough'  # This will include all the other columns in the output
    )

    pipeline = [('clipping_rooms', pp.ClippingColumn(column='rooms', quantile=0.95)),
                            ('clipping_garages', pp.ClippingColumn(column='garages', quantile=0.95)),
                            ('clipping_useful_area', pp.ClippingColumn(column='useful_area', quantile=0.95)),
                            ('other_category_bairro', pp.OthersCategoryTransformer(column='bairro', low_threshold=0.01)),
                            ('OneHotEncoding', transform_categorical)
                            ]
    grid_search = {
        'clipping_rooms__quantile': [None, 0.95, 0.9],
        'clipping_garages__quantile': [None, 0.95, 0.9],
        'clipping_useful_area__quantile': [None, 0.95, 0.9],
        'other_category_bairro__low_threshold': [None, 0.01, 0.05]
    }
    return pipeline, grid_search


class BuildFeatures_CV(BaseEstimator, TransformerMixin):
    """"
    Class used to create features that need to be cross validated to prevent Data Leakage.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X
    
class BuildFeatures(BaseEstimator, TransformerMixin):
    """
    Class used to create features that not need to be cross validated to prevent Data Leakage
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X