from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, NumberRange

# Organizations


class OrganizationForm(FlaskForm):
    companyname = StringField('Razon Social',
                         id='company_name_org',
                         validators=[DataRequired()])
    companydesc = TextAreaField('Descripcion',
                             id='company_description_org',
                             validators=[DataRequired()])
    companycode = IntegerField('Codigo',
                            id='company_code_org',
                            validators=[DataRequired()])
    companytype = SelectField('Tipo de Organizacion',
                            id='company_type_org',
                            validators=None, coerce=int)
                           


class CreateOrganizationForm(FlaskForm):
    companyid   = IntegerField('Company Id',
                         id='company_id_org',
                         validators=[NumberRange(1, 999999)])
    companyname = StringField('Razon Social',
                         id='company_name_org',
                         validators=[DataRequired()])
    companydesc = StringField('Descripcion',
                             id='company_description_org',
                             validators=[DataRequired()])
    companycode = IntegerField('Codigo',
                            id='company_code_org',
                            validators=[DataRequired()])
    companytype = SelectField('Tipo de Organizacion',
                            id='company_type_org',
                            validators=None, coerce=int)
    createdat   = StringField('Creada el',
                            id='created_at_org',
                            validators=None )
    companystat = IntegerField('Estatus',
                            id='company_estatus_org',
                            validators=None)
