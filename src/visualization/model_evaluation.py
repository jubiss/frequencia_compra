# Check yellow brick for model evaluation and visualization
import sys,os
sys.path.append(os.getcwd())
from src.utils import utils
import pandas as pd
def evaluate_model(model_type, y_true, y_pred, train_model=''):
    if model_type == 'classification':
        from sklearn.metrics import classification_report
        report = classification_report(y_true, y_pred, output_dict=True)
        df = pd.DataFrame(report).transpose()
        utils.save_csv(df, filepath_name=f'models/metrics/metrics_{train_model}.csv')
        
    if model_type == 'regression':
        from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, median_absolute_error, mean_absolute_error, r2_score
        metrics = []
        metrics.append(mean_squared_error(y_true, y_pred))
        metrics.append(mean_absolute_percentage_error(y_true, y_pred))
        metrics.append(median_absolute_error(y_true, y_pred))
        metrics.append(mean_absolute_error(y_true, y_pred))
        metrics.append(r2_score(y_true, y_pred))
        columns = ['mean_squared_error_', 'mean_absolute_percentage_error_', 'median_absolute_error_', 'mean_absolute_error_', 'r2_score_']
        df = pd.DataFrame([metrics], columns=columns)
        utils.save_csv(df, filepath_name=f'models/metrics/metrics_{train_model}.csv', save=True)

def evaluate_kpis(y_true, y_pred, model, threshold=0.2, save=False):

    absolute_percentage_error = abs(y_true - y_pred)/y_true
    mean_absolute_percentage_error = absolute_percentage_error.mean()
    error_higher_than_threshold = absolute_percentage_error[absolute_percentage_error > threshold].count()
    if save:
        kpis = pd.read_csv('models/main_kpis.csv')
        new_kpis = pd.DataFrame(data=[[model, mean_absolute_percentage_error, error_higher_than_threshold]],columns=['model', 'mean_abs_percentage_error', 'error_higher_than_threshold'])
        kpis = pd.concat([kpis, new_kpis])
        kpis.to_csv('models/main_kpis.csv', index=False)
    else:
        print(mean_absolute_percentage_error, error_higher_than_threshold)
    return mean_absolute_percentage_error, error_higher_than_threshold