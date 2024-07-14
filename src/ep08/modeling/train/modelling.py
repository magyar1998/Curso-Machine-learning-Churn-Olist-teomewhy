import pandas as pd
import os
import sqlalchemy
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder
import pickle


MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING = os.path.dirname(MODEL_DIR)
BASE_DIR = os.path.dirname(MODELLING)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')
MODEL_DIR = os.path.join(BASE_DIR , 'models')


engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table('tb_abt_churn', engine)

# Supondo que 'abt' é o DataFrame original
df_oot = abt[abt['dt_ref'] == abt['dt_ref'].max()].copy()
df_abt = abt[abt['dt_ref'] < abt['dt_ref'].max()].copy()

target = 'flag_compra'
to_remove = ['dt_ref', 'seller_id', 'dt_ref:1', 'seller_id:1', 'seller_city', target]

features = df_abt.columns.tolist()

for f in to_remove:
    if f in features:
        features.remove(f)

x_train, x_test, y_train, y_test = train_test_split(df_abt[features], df_abt[target], test_size=0.2, random_state=1998)

categorical_features = df_abt[features].select_dtypes('object').columns.to_list()
numerical_features = list(set(features) - set(categorical_features))

ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
ohe.fit(x_train[categorical_features])


ohe_train_df = pd.DataFrame(ohe.transform(x_train[categorical_features]), columns=ohe.get_feature_names_out(categorical_features))
ohe_test_df = pd.DataFrame(ohe.transform(x_test[categorical_features]), columns=ohe.get_feature_names_out(categorical_features))


x_train.reset_index(drop=True, inplace=True)
x_test.reset_index(drop=True, inplace=True)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)


df_train = pd.concat([x_train[numerical_features], ohe_train_df], axis=1)
df_test = pd.concat([x_test[numerical_features], ohe_test_df], axis=1)
features_fit = df_train.tolist()


df_train.columns = df_train.columns.astype(str)
df_test.columns = df_test.columns.astype(str)


y_train.name = str(y_train.name)
y_test.name = str(y_test.name)

print(df_train.shape)

clf = DecisionTreeClassifier()
clf.fit(df_train, y_train)

y_train_prob = clf.predict_proba(x_train)
y_train_pred = clf.predict(x_train)

print('\n')
print('Acurácia do treino', accuracy_score(y_train, y_train_pred))
print('Acurácia do roc', roc_auc_score(y_train, y_train_prob[:, 1]))


y_test_prob = clf.predict_proba(x_test)
y_test_pred = clf.predict(x_test)
print('\n')
print('Acurácia do test', accuracy_score(y_test, y_test_pred))
print('Acurácia do roc', roc_auc_score(y_test, y_test_prob[:, 1]))

y_oot_prob = clf.predict_proba(df_oot[features])
y_oot_pred = clf.predict(df_oot[features])
print('\n')
print('Acurácia do oot', accuracy_score(df_oot[target], y_oot_pred))
print('Acurácia do roc', roc_auc_score(df_oot[target], y_oot_prob[:, 1]))


df_abt_onehot = pd.DataFrame(OneHotEncoder.transform(df_abt[categorical_features]), 
                             columns=OneHotEncoder.get_feature_names_out(categorical_features))

df_abt_predict = pd.concat(abt[numerical_features], df_abt_onehot, axis = 1)

probs = clf.predict_proba(df_abt_predict)

abt['score_churn'] = probs[:, 1]


abt_score = abt[['dt_ref', 'seller_id','score_churn']]
abt_score.to_sql('tb_score_churns', engine, index=False, if_exists='replace')


model_data = pd.Series({

        'num_features': numerical_features,
        'cat_features':categorical_features,
        'ohe': OneHotEncoder,
        'features': features_fit,
        'model': clf,
        'acc_train': accuracy_score(y_train, y_train_pred),
        'acc_test': accuracy_score(y_test, y_test_pred),
        'acc_oot':  accuracy_score(df_oot[target], y_oot_pred)
})


model_data.to_pickle(os.path.join(MODEL_DIR, 'arvore_decisao.pkl'))

