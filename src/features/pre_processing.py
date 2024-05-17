from sklearn.base import BaseEstimator, TransformerMixin

def OneHotEncoderTransformerSelectedColumns(categorical_features):

    from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
    from sklearn.compose import ColumnTransformer
    enc = OneHotEncoder(handle_unknown='ignore')
    categorical_features = categorical_features

    transform_categorical = ColumnTransformer(
        transformers=[
            ('OneHotEncoder', enc, categorical_features),
        ],
        remainder='passthrough'  # This will include all the other columns in the output
    )
    return transform_categorical

class ClippingColumn(BaseEstimator, TransformerMixin):
    def __init__(self, column, quantile):
        self.column = column
        self.quantile = quantile
        self.quantile_value = None
    
    def fit(self, X, y=None):
        if self.quantile is None:
            return self
        elif self.quantile <= 1 and self.quantile >= 0:
            self.quantile_value = self.quantile_value_(X, self.column, self.quantile)
            return self

    def transform(self, X, y=None):
        if self.quantile is None:
            return X
        elif self.quantile >= 0.5:
            X.loc[X[self.column] > self.quantile_value,self.column] = self.quantile_value
        elif self.quantile < 0.5:
            X.loc[X[self.column] < self.quantile_value,self.column] = self.quantile_value
        return X

    def quantile_value_(self, X, column, quantile):
        quantile_value_ = X[column].quantile(quantile)
        return quantile_value_

class OthersCategoryTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column, low_threshold=0.05):
        self.column = column
        self.low_threshold = low_threshold
        self.category_transformer = None

    def fit(self, X, y=None):
        # Get the value counts normalized
        if self.low_threshold is None:
            return self
        elif self.low_threshold <= 1 and self.low_threshold >= 0:
            category_transformer = X[self.column].value_counts(normalize=True).reset_index()
            category_transformer.columns = [self.column, 'frequency']
            category_transformer[f'{self.column}_other'] = category_transformer[self.column]
            category_transformer.loc[category_transformer['frequency'] < self.low_threshold, f'{self.column}_other'] = 'Other'
            self.category_transformer = category_transformer
            return self
        else:
            raise ValueError ("Invalid low threshold value")

    def transform(self, X, y=None):
        if self.low_threshold is None:
            return X
        else:        
            X = X.merge(self.category_transformer[[self.column, f'{self.column}_other']], how='right', on=self.column)
            X = X.drop(columns=self.column)
            X = X.rename(columns={f'{self.column}_other': self.column})
        
        return X

class PreProcessingFeatures(BaseEstimator, TransformerMixin):
    """Class used to make all the preprocessing steps for the model to work properly"""
    def __init__(self, scale_dict=None):
        self.scale_dict = scale_dict
        if scale_dict:
            for column in scale_dict.keys():
                self.scale_columns, self.scale_quantiles = column, scale_dict[column]

    def fit(self,X, y=None):
        pass

    def transform(self,X, y=None):
        pass

    def missing_values(self, X, y):
        # Dealing with missing values
        pass

    def transforming_data(self, X, y):
        # Transforming data
        pass

    def scaling_data(self, X, y):
        pass

    def enconding_data(self, X, y):
        pass

    def outliers(self, X, y):
        pass