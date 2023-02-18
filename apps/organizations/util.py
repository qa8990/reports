from datetime import datetime, date
from apps import db, props, sql_scripts
import requests, json, poplib
from pathlib import Path
import typing

API_URL = "http://127.0.0.1:8000/api/v1"
params = {'skip': '0', 'limit': '100'}
headers = {'Content-Type': 'application/json'}


# Return the current date like a String object
def get_current_date_time():
    now = datetime.now()   #Current date
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time

# Return the 
def get_last_company_added():
    statement = sql_scripts['org_sql_getlastcompanyadded']
    return statement

# new version
def get_json_data(apiMethod, path, skip, limit, json_data):
    
    data_json = json.dumps(json_data, indent=4) 
    payload = data_json
    url = f"{API_URL}{path}"
    params["skip"] = skip
    params["limit"] = limit
    print(" } JSON DATA { :", url, apiMethod, headers, payload, params)
    response = requests.request(apiMethod, url, headers=headers, data=payload, params=params)
    return response.json()

#old version
def get_json_data2(apiMethod, path, skip, limit, json_data):

    data_json = json.dumps(json_data, indent=4) 
    payload = data_json
    params["skip"] = skip
    params["limit"] = limit
    headers = {'Content-Type': 'application/json'}

    #if  skip == None: 
    #    url = '{0}{1}/'.format(API_URL, path)
    #    print("URL API 1> :", url)
    #else:
    #    url = '{0}{1}/{2}'.format(API_URL, path, params)
    #    print("URL API 2 > :", url, apiMethod, headers, payload)
    if  skip == None: 
        print("[ util - STEP 001 ]", datetime.now())
        url = '{0}{1}/'.format(API_URL, path)
        print("<---- 1 URL API 1 ----> :", url, apiMethod, headers, payload, params)
        #if apiMethod == 'GET':
        print("######### estoy en el method = GET")
        response = requests.request(apiMethod, url, headers=headers, data=payload)
        #else:
        #    print("@@@@@@@@@@ estoy en el method = POST")
        #    response = requests.post(url, headers=headers, data=payload)
        #response = requests.post(apiMethod, url, headers=headers, json=payload)
    else:
        print("[ util - STEP 002 ]", datetime.now())
        url = '{0}{1}/'.format(API_URL, path)
        print("<===== 2 URL API 2 ====> :", url, apiMethod, headers, payload, params)
        #if apiMethod == 'GET':
        response = requests.request(apiMethod, url, params=params, data=payload, headers=headers)
        #else:
        #    response = requests.post(url, params=params, json=payload)
    print(" response =================>>>>>>>>>>> ",response, type(response))
    return response.json()

def format_json_object(json_data: dict, id: int):
    new_dict = {}
    json_data.pop("csrf_token")
    json_data.pop("Actualizar")
    #json_data.pop("created_at")
    keys = ('company_id', 'name', 'description', 'company_type_id', 'code', 'created_at', 'status_id')
    #keys = ('name', 'description', 'company_type_id', 'code', 'created_at', 'status_id')
    new_dict = json_data.fromkeys(keys)
    new_dict.update({"company_id": 0})
    new_dict.update({"name": json_data.get("name")})
    new_dict.update({"description": json_data.get("description")})
    new_dict.update({"code": json_data.get("code")})
    new_dict.update({"company_type_id": json_data.get("company_type_id")})
    new_dict.update({"created_at": json_data.get("created_at")})
    new_dict.update({"status_id": json_data.get("status_id")})
    #if id != None:
    #    new_dict.update({"company_id": id})
    return new_dict

def format_json_object2(json_data: dict, id: int):
    new_dict = {}
    json_data.pop("csrf_token")
    json_data.pop("Actualizar")

    #json_data.pop("created_at")
    keys = ('name', 'description', 'company_type_id', 'code')
    #keys = ('name', 'description', 'company_type_id', 'code', 'created_at', 'status_id')
    new_dict = json_data.fromkeys(keys)
    new_dict.update({"name": json_data.get("name")})
    new_dict.update({"description": json_data.get("description")})
    new_dict.update({"code": json_data.get("code")})
    new_dict.update({"company_type_id": json_data.get("company_type_id")})

    #if id != None:
    #    new_dict.update({"company_id": id})
    return new_dict
