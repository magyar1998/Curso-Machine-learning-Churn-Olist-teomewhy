import pandas as pd
import os
import sqlalchemy
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING = os.path.dirname(MODEL_DIR)
BASE_DIR = os.path.dirname(MODELLING)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')


engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

abt = pd.read_sql_table('tb_abt_churn', engine)

# print(abt.columns)
df_oot = abt[abt['dt_ref'] == abt['dt_ref'].max()].copy()
df_abt = abt[abt['dt_ref'] < abt['dt_ref'].max()].copy()


target = 'flag_compra'
to_remove = ['dt_ref', 'seller_id', 'dt_ref:1', 'seller_id:1','seller_city', 'seller_state', target]

features = df_abt.columns.tolist()

for f in to_remove:
    if f in features:
        features.remove (f)


x_train, x_test, y_train, y_test = train_test_split(df_abt[features],
                                                    df_abt[target],
                                                    test_size=0.2,
                                                    random_state= 1998)

clf = DecisionTreeClassifier(min_samples_leaf=100)
clf.fit(x_train,y_train)

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