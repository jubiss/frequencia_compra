import sys,os
sys.path.append(os.getcwd())
import pandas as pd
from src.utils import utils

def feature_importance(model, cv_result, train_name=''):
    if model == 'LinearRegression':
        coeficients = cv_result.best_estimator_['model'].coef_
        intercept = cv_result.best_estimator_['model'].intercept_
        feature_names = cv_result.best_estimator_.named_steps.OneHotEncoding.get_feature_names_out()
        feature_names = [name.split('__')[-1] for name in feature_names]
        coefficients = pd.DataFrame([coeficients], columns=feature_names)
        coefficients['intercept'] = intercept
        utils.save_csv(coefficients, filepath_name=f'models/lin_reg_coef_{train_name}.csv', save=True)
    else:
        pass