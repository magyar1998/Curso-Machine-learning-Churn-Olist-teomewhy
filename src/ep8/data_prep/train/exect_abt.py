import os
import sqlalchemy

TRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PREP = os.path.dirname(TRAIN_DIR)
BASE_DIR = os.path.dirname(DATA_PREP)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')

engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

with open (os.path.join(TRAIN_DIR, 'criacao_abt.sql'), 'r') as open_file:
    query = open_file.read()


for q in query.split(";")[:-1]:
    with engine.connect() as connection:
        with connection.begin() as transaction: 
            connection.execute( sqlalchemy.text( q ))
