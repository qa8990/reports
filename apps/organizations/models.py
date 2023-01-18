from flask_login import UserMixin

from apps import db

from apps.organizations.util import get_current_date_time
from datetime import time, datetime
from sqlalchemy.orm import relationship, backref

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