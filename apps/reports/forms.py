from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, widgets, validators
from wtforms.validators import Email, DataRequired, NumberRange

# Organizations


class ReportsForm(FlaskForm):
    id =                    IntegerField('Id',
                                id='account_id',
                                validators=[DataRequired()])
    account_number =        StringField('Nro de Cuenta',
                                id='account_number',
                                validators=[DataRequired()])
    account_name =          StringField('Cuenta',
                                id='account_name',
                                validators=[DataRequired()])
    status_id =             IntegerField('Estatus',
                                id='company_estatus_org',
                                validators=None)                            
                           

