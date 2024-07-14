import pandas as pd
import os
import sqlalchemy
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING = os.path.dirname(MODEL_DIR)
BASE_DIR = os.path.dirname(MODELLING)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')
MODEL_DIR = os.path.join(BASE_DIR , 'models')


engine  = sqlalchemy.create_engine('sql:///' + os.path.join(DATA_DIR, 'olist.db'))

query  = 'select * tb_book_sellers where dt_ref = "2018-06-01"'

data = pd.read_sql_query(query, engine)

model = pd.read_pickle(os.path.join(MODEL_DIR, 'arvore_decisao.plk'))

df_onehot = pd.DataFrame(model['ohe'].transform(data[model['cat_features']]),
                        columns= model['ohe'].get_feature_names_(model['cat_features']))

df_predict = pd.concat([data[model['num_features']], df_onehot], axis=1)

data['score_churn'] = model['model'].predict_proba(df_predict[model['features']])[:, 1]

data_score = data[['dt_ref','seller_id' ,'score_churn']]

data_score.to_sql('tb_churn_score', engine, index=False, if_exists='replace')

