from datetime import datetime, date
from apps import db, props, sql_scripts

# Return the current date like a String object
def get_current_date_time():
    now = datetime.now()   #Current date
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time

# Return the 
def get_last_company_added():
    statement = sql_scripts['org_sql_getlastcompanyadded']
    print(statement, 'La estatement de hoy')
    return statement