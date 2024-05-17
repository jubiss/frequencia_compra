import sys,os
sys.path.append(os.getcwd())
import pandas as pd
import src.models.train_model as train

model_type = 'regression'

datapath = 'data\processed\listings_with_address.csv'
columns = ['rooms', 'garages', 'useful_area', 'value', 'interior_quality', 'bairro']
treated_df = pd.read_csv(datapath)[columns]
target = 'value'
model_name = 'DummyRegressor'
train_name = 'DummyModel_'
train.train_save_model(treated_df, target, model_name, train_name=train_name, 
                       model_type='regression')