import os
import sys
from src.exception import CustomException
import dill

import numpy as np
import pandas as pd
from src.logger import logging

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model =  list(models.values())[i]
            para = param[list(models.keys())[i]]


            logging.info(f"Starting GridSearchCV on {model} to find the best parameter for the model")
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            logging.info("Performed the grid search")
            model.set_params(**gs.best_params_)
            logging.info(f'Found the best parameter for {model} and giving it to model')
            model.fit(x_train,y_train)


            #model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred  = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score  = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e,sys)
    