from apps.organizations.models import Companies, CompaniesTypes
from apps.masterplan.models import MasterPlan
from sqlalchemy import func, select
from apps import db
from apps.utils.stocks_properties import read_master_plan
import pandas as pd

def create_new_company(company):

    db.session.add(company)
    db.session.commit()
    return 

def create_new_account(account):
    
    db.session.add(account)
    db.session.commit()
    return 

def clean_master_plan():
    #masterplan = MasterPlan()
    #masterplan = db.session.execute(db.select(masterplan.account_name)).all()
    db.session.query(MasterPlan).delete()
    db.session.commit()
    #statement = "update sqlite_sequence set seq=0 where name='master_plan'"
    #db.session.execute(statement)
    #db.session.commit()
    return

def upload_master_plan():
    df = read_master_plan()
    
    for i in range(len(df)):
        masterplan = MasterPlan()
        masterplan.account_number = int(df.iloc[i]['nrocuenta'])
        masterplan.account_name = df.iloc[i]['cuenta']
        masterplan.status_id=1
        create_new_account(masterplan)
        #db.session.add(masterplan)
        #db.session.commit()

    return
        