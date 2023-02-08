from datetime import datetime, date
from apps import db, props, sql_scripts
import requests
from pathlib import Path
import typing

API_URL = "http://127.0.0.1:8000/api/v1"


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


def get_json_data(path, url_parms):

    
    payload={}
    #body=None
    headers = {'Content-Type': 'application/json'}

    if  url_parms == None: 
        url = '{0}{1}/'.format(API_URL, path)
    else:
        url = '{0}{1}/{2}'.format(API_URL, path, url_parms)
    print("url >>>",url, url_parms)
    response = requests.request("GET", "http://127.0.0.1:8000/api/v1/companies/?skip=0&limit=100", headers=headers, data=payload)
    #response = requests.request("GET", url, headers=headers, data=payload)
    print("---------    J S O N ------------->")
    #print( response.json())
    return response.json()

