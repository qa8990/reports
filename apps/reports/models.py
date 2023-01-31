from flask_login import UserMixin

from apps import db

from apps.organizations.util import get_current_date_time
from datetime import time, datetime
from sqlalchemy.orm import relationship, backref, query
from sqlalchemy import func, select
from apps.organizations.models import Status



class ReportsForma(db.Model):

    __tablename__ = 'report_forma'

    forma_code = db.Column(db.String(1), primary_key=True)
    forma_name = db.Column(db.String(60))
    forma_description = db.Column(db.String(200))
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

            if property == 'status_id':
                value = 1

            print("setattr  *********** > ", self, 'properpty : ', property, 'Value : ',  value)
            setattr(self, property, value)

            #### REVISAR los metods que faltan aca ##################################   <------------------
            ######## @#$243234234234234
            ### comparar como lo usasn en authentication

    def __repr__(self):
        return str(self.forma_name)


    def get_all():
        forma = db.session.execute(select(ReportsForma.forma_code, ReportsForma.forma_name, ReportsForma.forma_description, Status.description).join(Status.estatus)).all()
        #page1 = MasterPlan.query.paginate(page=page_nbr, per_page=10)
        #print("page1", page1.items)
        print('get-all forma ## ', forma)
        return forma


    def get_forma_byCode(code):
        forma = db.session.execute(select(ReportsForma.forma_code, ReportsForma.forma_name, ReportsForma.forma_description).filter_by(forma_code=code)).all()
        #print('get-by id ', account, type(account))
        # Companies.query.all()
        return forma


    def update_forma_byCode(self, id):
        print("estoy actualizando la company :", type(self.data) )
        statement = 'UPDATE master_plan SET account_number = :parm1, account_name = :parm2 where id = :parm3'
        account = db.session.execute(statement, {'parm1' : self.account_number.data, 'parm2' : self.account_name.data, 'parm3' : id, })
        db.session.commit()
        return 
    
    def create_forma(forma):
        print("estoy creando la cuenat :", type(forma) )
        db.session.add(ReportsForma(forma))
        db.session.commit()
        return 
        




