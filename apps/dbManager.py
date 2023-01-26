from apps.organizations.models import Companies, CompaniesTypes
from sqlalchemy import func, select
from apps import db

def create_new_company(company):

    db.session.add(company)
    db.session.commit()
    return 

    