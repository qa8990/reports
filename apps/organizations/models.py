from flask_login import UserMixin

from apps import db

from apps.organizations.util import get_current_date_time
from datetime import time, datetime
from sqlalchemy.orm import relationship, backref, query
from sqlalchemy import func, select
class Companies(db.Model):

    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    code = db.Column(db.Integer, unique=True)
    company_type_id = db.Column(db.Integer, db.ForeignKey("company_types.company_type_id"))
    #company_type_id = relationship("CompaniesTypes", lazy='joined', backref=backref("type"))
    created_at = db.Column(db.String(20))
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)

            if property == 'created_at':
                value = get_current_date_time()  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)

    def get_all():
        companies = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at).join(CompaniesTypes.type)).all()
        print('get-all ', companies)
        # Companies.query.all()
        return companies

    def get_company_byId(id):
        
        company = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at).join(CompaniesTypes.type).filter_by(company_id=id)).all()
        print('get-by id ', company, type(company))
        # Companies.query.all()
        return company

    def get_last_company_added():
        print('last companie added')
        max_date = db.session.query(func.max(Companies.created_at)).scalar()
        last_company_added = Companies.query.filter_by(created_at = max_date).one()
        #db.session.query(Companies).filter(Companies.created_at == max_date).all()
        print(max_date)
        print('last-company-date :::::>',last_company_added)
        return last_company_added


def organization_loader(id):
    print('***** en el loader de organization ********')
    return Companies.query.filter_by(company_id=id).first()



def request_loader(request):
    id = request.form.get('companyid')
    print('$$$$$$$$ --> ',id)
    company = Companies.query.filter_by(company_id=id).first()
    print('#### User >', company)
    return company if company else None


class CompaniesTypes(db.Model):
    
    __tablename__ = 'company_types'

    company_type_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    description = db.Column(db.String(64), unique=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.status_id"), nullable=False)
    image = db.Column(db.String(64))
    type = db.relationship("Companies", backref="type", lazy=True)
    #products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.company_type_id)


class Status(db.Model):
    
    __tablename__ = 'status'

    status_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(64))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.status_id)