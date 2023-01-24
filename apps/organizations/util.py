from datetime import datetime
from apps import db, props, sql_scripts


def get_current_date_time():
    date_time= datetime
    print('date y teime', date_time)
    return date_time

def get_last_company_added():
    statement = sql_scripts['org_sql_getlastcompanyadded']
    print(statement, 'La estatement de hoy')
    return statement