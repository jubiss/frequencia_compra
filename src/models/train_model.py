import sys,os
sys.path.append(os.getcwd())
import joblib
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import src.features.feature_pipe as features
import src.models.ml_models as ml_models
from src.visualization import explainability, model_evaluation

def train_save_model(df, target, model_name, train_name='', model_type='regression'):

    X, y = df.drop(columns=target), df[target]

    feature_pipe, feature_grid = features.features_pipeline()

    model, ml_grid = ml_models.get_model(model_name)

    pipeline = feature_pipe
    pipeline.extend([("model", model)])
    pipe_grid = {}
    pipe_grid.update(feature_grid)
    pipe_grid.update(ml_grid)
    #boruta_selector = BorutaPy(model_, n_estimators='auto', verbose=2, random_state=1)
    pipeline = Pipeline(pipeline)
    cv_result = GridSearchCV(pipeline, feature_grid, cv=5)
    cv_result.fit(X, y)

    explainability.feature_importance(model=model_name, cv_result=cv_result,
                                      train_name=train_name)
    predict = cv_result.predict(X)
    model_evaluation.evaluate_model(model_type=model_type, y_true=y,
                                    y_pred=predict, train_model=train_name)
    
    model_evaluation.evaluate_kpis(y_true=y, y_pred=predict, model=train_name,
                                   save=True)

    # Save Model
    joblib.dump(cv_result, f'models\pickle\model_{train_name}.pickle')