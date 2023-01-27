from apps.organizations.models import Companies, CompaniesTypes
from apps.masterplan.models import MasterPlan
from sqlalchemy import func, select
from apps import db

def create_new_company(company):

    db.session.add(company)
    db.session.commit()
    return 

def create_new_account(account):
    
    db.session.add(account)
    db.session.commit()
    return 

    