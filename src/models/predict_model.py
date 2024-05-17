import sys,os
sys.path.append(os.getcwd())
import joblib

from config import final_model_name

def batch_predict(data, train_name, data_with_predict=''):

    model = joblib.load(f'models/model_{train_name}.pickle')

    prediction = model.predict(data)
    data['prediction'] = prediction
    data.to_csv('data/predicted/pred_{train_name}_{data_with_predict}.csv')

def single_predict(data, train_name):

    model = joblib.load(f'models/model_{train_name}.pickle')

    prediction = model.predict(data)
    return prediction