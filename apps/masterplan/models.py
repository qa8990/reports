from flask_login import UserMixin

from apps import db

from apps.organizations.util import get_current_date_time
from datetime import time, datetime
from sqlalchemy.orm import relationship, backref, query
from sqlalchemy import func, select



class MasterPlan(db.Model):

    __tablename__ = 'master_plan'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20))
    account_name = db.Column(db.String(200))
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=True )

    def __init__(self, **kwargs):
        print("Registrando un companies  !!!!!!!!!!", self, type(self))
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'status_id':
                value = 1

            print("setattr  *********** > ", self, 'properpty : ', property, 'Value : ',  value)
            setattr(self, property, value)

            #### REVISAR los metods que faltan aca ##################################   <------------------
            ######## @#$243234234234234
            ### comparar como lo usasn en authentication

    def __repr__(self):
        return str(self.account_name)


    def get_all(page_nbr):
        accounts = db.session.execute(select(MasterPlan.id, MasterPlan.account_number, MasterPlan.account_name)).all()
        page1 = MasterPlan.query.paginate(page=page_nbr, per_page=10)
        print("page1", page1.items)
        print('get-all ', page1)
        return page1

    def get_alls():
        accounts = db.session.execute(select(MasterPlan.id, MasterPlan.account_number, MasterPlan.account_name)).all()
        page1 = MasterPlan.query.all()
        return page1

    def get_account_byId(id):
        account = db.session.execute(select(MasterPlan.id, MasterPlan.account_number, MasterPlan.account_name).filter_by(id=id)).all()
        print('get-by id ', account, type(account))
        # Companies.query.all()
        return account


    def update_account_byId(self, id):
        print("estoy actualizando la company :", type(self.data) )
        statement = 'UPDATE master_plan SET account_number = :parm1, account_name = :parm2 where id = :parm3'
        account = db.session.execute(statement, {'parm1' : self.account_number.data, 'parm2' : self.account_name.data, 'parm3' : id, })
        db.session.commit()
        return 
    
    def create_account(account):
        print("estoy creando la cuenat :", type(account) )
        db.session.add(MasterPlan(account))
        db.session.commit()
        return 
        

def masterplan_loader(id):
    print('***** en el loader de organization ********')
    return MasterPlan.query.filter_by(id=id).first()



def request_loader(request):
    id = request.form.get('id')
    print('REQUES LOADER de Companies ^^^^^^^<..> <..> <..> <..> <<..>>  --> ',id)
    account = MasterPlan.query.filter_by(id=id).first()
    print('#### User >', account)
    return MasterPlan if account else None


