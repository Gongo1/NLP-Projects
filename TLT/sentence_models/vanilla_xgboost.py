#Vanilla XGBoost Script
#Author: Vince Trost
#Date: 1/17/2017

###### ASSUMPTIONS ######
#data must be preprocessed and model-ready

import xgboost as xgb
import numpy as np
import pandas as pd
import os
import sys
import getopt

def getArgs(argv):

    input_path  = ''          #path of input file(s)
    drop_colnames = ''      #column names to drop (comma separated)
    model_name = ''         #what you want to name the model OR path to model if task is inference
    y_col = ''           #name of the column that's being predicted
    task = ''               #train or infer

    try:
        opts, args = getopt.getopt(argv,"hi:d:m:y:t:",["input_path=","drop_colnames=","model_name=","y_col=","task="])
    except getopt.GetoptError:
        print 'usage: vanilla_xgboost.py -i <input_path> -d <drop_colnames> -m <model_name> -y <y_col> -t <task>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'usage: vanilla_xgboost.py -i <input_path> -d <drop_colnames> -m <model_name> -y <y_col> -t <task>'
            print '<task> can be either \'train\' or \'infer\''
            sys.exit()
        elif opt in ("-i", "--input"):
            input_path= arg
        elif opt in ("-d", "--drop_colnames"):
            drop_colnames = arg
        elif opt in ("-m", "--model_name"):
            model_name = arg
        elif opt in ("-y", "--y_col"):
            y_col = arg
        elif opt in ("-t", "--task"):
            task = arg
    #now we return the variables to be passed forward
    return (input_path,drop_colnames,model_name,y_col,task)

def get_params():

    params = {}
    params["objective"] = "reg:linear"
    params["eta"] = 0.02
    params["subsample"] = 1
    params["colsample_bytree"] = 1
    params["silent"] = 1
    params["max_depth"] = 10
    params["eval_metric"] = "rmse"
    params["gamma"] = 0.02
    params["booster"] = 'gbtree'
    plst = list(params.items())

    return plst

def cv_train(data, y_col):
    y_train = data[[y_col]]
    x_train = data.drop(y_col, axis=1)
    xg_train = xgb.DMatrix(x_train, label=y_train)
    nfolds = 5
    early_stopping = 10
    params = get_params()
    print('Initializing Cross-Validation Training... \n')
    cv = xgb.cv(params,
                xg_train,
                5000,
                nfold=nfolds,
                early_stopping_rounds=early_stopping,
                verbose_eval=1)
    print('Cross-Validation Training Finished.')
    best_iteration = cv.shape[0]
    return best_iteration

def train(data, y_col, best_iteration):
    y_train = data[[y_col]]
    x_train = data.drop(y_col, axis=1)
    dtrain = xgb.DMatrix(x_train, label=y_train)
    #train the model
    params = get_params()
    early_stopping = 10
    num_round = best_iteration
    watchlist = [(dtrain, 'train')]
    print('Initializing Regular Training with Best Iteration saved from CV Training... \n')
    model = xgb.train(params,
                        dtrain,
                        num_round,
                        watchlist,
                        early_stopping_rounds = early_stopping,
                        verbose_eval = 1)
    print('Regular Training Finished.')
    return model

def infer(data, model_name):
    model = xgb.Booster(model_file = str(model_name))
    dtest = xgb.DMatrix(data)
    print('Initializing Inference... \n')
    preds = model.predict(dtest)
    print('Inference Finished.')
    preds = pd.DataFrame(preds)
    preds.columns = ['Prediction']
    return preds


#Now we just want to use the CV training to find best iteration, record it, and run full training for that many iterations
#get predictions from original data (bad, but we just want something for the formatting)

def main():
    argv = sys.argv[1:]
    (input_path,drop_colnames,model_name,y_col,task) = getArgs(argv)
    data = pd.read_csv(input_path)
    flag = False
    if drop_colnames:
        flag = True
        drops = data[[drop_colnames]]
        data = data.drop(drop_colnames, axis=1)
    if task == 'train':
        #call xgb train cv function
        best_iteration = cv_train(data, y_col)
        model = train(data, y_col, best_iteration)
        model.save_model(str(model_name) + '.model')
    elif task == 'infer':
        #call xgb infer function
        preds = infer(data, model_name)
        zip the predictions back up with the original file
        if flag:
            frames = [drops, data, preds]
            master = pd.concat(frames, axis=1)
        else:
            frames = [data, preds]
            master = pd.concat(frames, axis=1)

        master.to_csv('preds.csv', sep=',', index=False)

    else:
        print('Invalid entry for -t or --task. Must be either \'train\' or \'infer\'.')


if __name__ == '__main__':
    main()
