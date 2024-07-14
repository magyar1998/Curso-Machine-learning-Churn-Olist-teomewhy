import pandas as pd
import os
import sqlalchemy
import argparse
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING = os.path.dirname(MODEL_DIR)
BASE_DIR = os.path.dirname(MODELLING)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')
MODEL_DIR = os.path.join(BASE_DIR , 'models')


DBPATH = r"Home\Machine Learning\data\olist.db"

parser = argparse.ArgumentParser()
parser.add_argument('--dt_ref', help = 'Data de referência para a safra a ser predita: YYYY-MM-DD')
args = parser.parse_args()

print('importando modelo...', end='')
model = pd.read_pickle(os.path.join(MODEL_DIR, 'model_churn.pkl'))
print('ok.')


print('Abrindo conexão com o banco de dados...', end='')
con = sqlalchemy.create_engine('sql:///' + DBPATH)
print('ok.')


print('importando dados...', end='')
query = f"SELECT * FROM tb_book_sellers WHERE dt_ref = '{args.dt_ref}';"
df = pd.read_sql_query(query, con)
print('ok.')

print('Preparando dados para aplicar modelo...', end='')

df_onehot = pd.DataFrame(model['onehot'].transform(df[model['cat_features']]), columns = model['onehot'].get_features_names(model['cat_features']))
df_full = pd.concat([df[model['num_features']], df_onehot], axis=1)
df_full = df_full[model['features_fit']]
print('ok.')


print('Criando score...', end='')
df['score'] = model['model'].predict_proba(df_full)[:, 1]
print('ok.')


print('Enviando os dados para o banco de dados...', end='')
df_score = df[['df_ref', 'seller_id', 'score']]
df_score['dt_atualização'] = datetime.datetime.now()
df_score.to_sql('tb_churn_score', con, if_exists='replace', index=False)
print('ok.')




