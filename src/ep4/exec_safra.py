import pandas as pd
import sqlalchemy
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--date", "-d", help= "Data de referência no formato YYYY-MM-dd")

args = parser.parse_args()
date = args.date

ep_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.dirname(ep_dir)
base_dir = os.path.dirname(src)
data_dir = os.path.join(base_dir, 'data')



def import_query(path, **kwards):
    with open (path, 'r', **kwards) as file_open:
        result = file_open.read()
    return result

query = import_query(os.path.join(ep_dir, 'query_4.sql'))
query = query.format(date = date)

# print(query)

engine = sqlalchemy.create_engine('sqlite:///' + os.path.join(data_dir, 'olist.db'))

print(data_dir)

try:
    print('Tentando deletar...\n')
    with engine.connect() as connection:
        connection.execute( sqlalchemy.text('delete from tb_book_sellers where dt_ref = {date}'.format(date = date)))
    print('ok')
except:
    print('tabela não encontrada')

try:
    base_query = 'create table tb_book_sellers as\n {query}'
    with engine.connect() as connection:
        connection.execute( sqlalchemy.text(base_query.format(query  = query)))
except:
    base_query = 'insert into tb_book_sellers \n {query}'
    with engine.connect() as connection:
            with connection.begin() as transaction:
                connection.execute(sqlalchemy.text(base_query.format(query  = query))) 




