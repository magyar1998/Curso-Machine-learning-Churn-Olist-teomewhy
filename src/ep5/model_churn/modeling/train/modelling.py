import pandas as pd
import os
import sqlalchemy

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELLING = os.path.dirname(MODEL_DIR)
BASE_DIR = os.path.dirname(MODELLING)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), 'data')


engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(DATA_DIR, 'olist.db'))

