from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, widgets, validators
from wtforms.validators import Email, DataRequired, NumberRange

# Organizations


class OrganizationForm(FlaskForm):
    name =              StringField('Razon Social',
                            id='company_name_org',
                            validators=[DataRequired()])
    description =       TextAreaField('Descripcion',
                             id='company_description_org',
                             validators=[DataRequired()])
    code =              IntegerField('Codigo',
                            id='company_code_org',
                            validators=[DataRequired()])
    company_type_id =   SelectField('Tipo de Organizacion',
                            id='company_type_org',
                            validators=None, coerce=int)
    created_at   = StringField('Creada el',
                            id='created_at_org',
                            validators=None )
    status_id = IntegerField('Estatus',
                            id='company_estatus_org',
                            validators=None)                            
                           


class CreateOrganizationForm(FlaskForm):
    company_id   = IntegerField('Company Id',
                         id='company_id_org',
                         validators=[NumberRange(1, 999999)])
    name = StringField('Razon Social',
                         id='company_name_org',
                         validators=[DataRequired()])
    description = TextAreaField('Descripcion',
                             id='company_description_org',
                             validators=[DataRequired(), validators.length(max=200)],
                             )
    code = IntegerField('Codigo',
                            id='company_code_org',
                            validators=[DataRequired()])
    company_type_id = SelectField('Tipo de Organizacion',
                            id='company_type_org',
                            validators=None, coerce=int)
    created_at   = StringField('Creada el',
                            id='created_at_org',
                            validators=None )
    status_id = IntegerField('Estatus',
                            id='company_estatus_org',
                            validators=None)
