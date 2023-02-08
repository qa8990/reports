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
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True )

    def __init__(self, **kwargs):
        print("Registrando un companies  !!!!!!!!!!", self, type(self))
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'created_at':
                value = get_current_date_time()  # we need bytes here (not plain str)

            if property == 'status_id':
                value = 1

            print("setattr  *********** > ", self, 'properpty : ', property, 'Value : ',  value)
            setattr(self, property, value)

            #### REVISAR los metods que faltan aca ##################################   <------------------
            ######## @#$243234234234234
            ### comparar como lo usasn en authentication

    def __repr__(self):
        return str(self.name)


    def get_all():
        #companies = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at, Status.description).join(CompaniesTypes.type).join(Status.estatus)).all()
        #companies = db.session.query(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at, Status.description).join(CompaniesTypes.type).join(Status.estatus)).all()
       #subq = db.session.query(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at).join(CompaniesTypes.type)).all()
        statement = "SELECT companies.company_id, companies.name, companies.description, company_types.description AS description_1, company_types.image, companies.created_at, status.description AS description_2 FROM company_types JOIN companies ON company_types.company_type_id = companies.company_type_id JOIN  status  ON status.id = companies.status_id"
        companies = db.session.execute(statement)
        print('get-all ', companies)
        # Companies.query.all()
        return companies

    def get_company_byId(id):
        company = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at, Companies.code).join(CompaniesTypes.type).filter_by(company_id=id)).all()
        print('get-by id ', company, type(company))
        # Companies.query.all()
        return company

    def get_last_company_added():
        print('last companie added')
        max_date = db.session.query(func.max(Companies.created_at)).scalar()
        last_company_added = Companies.query.filter_by(created_at = max_date).first()
        #db.session.query(Companies).filter(Companies.created_at == max_date).all()
        print(max_date)
        print('last-company-date :::::>',last_company_added)
        return last_company_added

    def update_company_byId(self, id):
        print("estoy actualizando la company :", type(self.data) )
        statement = 'UPDATE companies SET name = :parm1, description = :parm2, code = :parm3, company_type_id = :parm4 where company_id = :parm5'
        company = db.session.execute(statement, {'parm1' : self.name.data, 'parm2' : self.description.data, 'parm3' : self.code.data, 'parm4' : self.company_type_id.data, 'parm5': id, })
        db.session.commit()
        return 
    
    def create_company(company):
        print("estoy creando la company :", type(company) )
        db.session.add(Companies(company))
        db.session.commit()
        return 
        

def organization_loader(id):
    print('***** en el loader de organization ********')
    return Companies.query.filter_by(company_id=id).first()



def request_loader(request):
    id = request.form.get('companyid')
    print('REQUES LOADER de Companies ^^^^^^^<..> <..> <..> <..> <<..>>  --> ',id)
    company = Companies.query.filter_by(company_id=id).first()
    print('#### User >', company)
    return company if company else None


class CompaniesTypes(db.Model):
    
    __tablename__ = 'company_types'

    company_type_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    description = db.Column(db.String(64), unique=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
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

    def get_all_company_types():
        company_types = db.session.execute(select(CompaniesTypes.company_type_id, CompaniesTypes.code, CompaniesTypes.description).where(CompaniesTypes.status_id == 1)).all()
        return company_types


class Status(db.Model):
    
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(64))
    estatus = db.relationship("ReportsForma", backref="estatus", lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.status_id)