import pandas as pd
import sqlalchemy
import os


ep_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.dirname(ep_dir)
base_dir = os.path.dirname(src)
data_dir = os.path.join(base_dir, 'data')

# para Jupyter
# print(os.path.abspath('.'))

print(data_dir)


def import_query(path, **kwards):
    with open (path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result

query = import_query(os.path.join(ep_dir, 'create_safra.sql'))

def connect_db():
    return sqlalchemy.create_engine('sqlite:///' + os.path.join(data_dir, 'olist.db'))

con = connect_db()

df = pd.read_sql(query, con)

print(df.head(5))