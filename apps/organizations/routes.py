from flask import render_template, redirect, request, url_for
from apps.organizations import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.organizations.forms import CreateOrganizationForm, OrganizationForm
from apps.organizations.models import Companies, CompaniesTypes

from apps.organizations.util import get_current_date_time

@blueprint.route('/')
def route_default():
    return redirect(url_for('organizations_blueprint.allcompanies'))


# Organization

@blueprint.route('/allcompanies', methods=['GET'])
def allcompanies():
    print('@@@ ### Allcompanies route ####  @@@')
    company_form = OrganizationForm()
        
    # Other style
    company = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description).join(CompaniesTypes.type)).all()
    print('@@@ ### Allcompanies route ####  @@@', company, type(company))

    # Check the password
    if company :
        return render_template('organizations/companies.html', company=company)

@blueprint.route('/editcompany/<id>', methods=['GET', 'POST'])
def editcompany(id):
    print("Estoy en edit company -->", id, type(int(id)))
    #company_form = OrganizationForm()
    comp_id = int(id)
    company_obj = Companies()
    edit_organization_form = OrganizationForm()
    if request.method == 'GET':

        statement = 'SELECT  company_id, name, description, code, company_type_id, created_at FROM companies where company_id = :parm1'
        company = db.session.execute(statement, {'parm1' : comp_id}).fetchone()
        
        company_types = db.session.execute(select(CompaniesTypes.company_type_id, CompaniesTypes.code, CompaniesTypes.description).where(CompaniesTypes.status_id == 1)).all()
        #company_obj = Companies(company)
        print(company_types)
        edit_organization_form.companyname.data = company[1]
        edit_organization_form.companydesc.data = company[2]
        edit_organization_form.companycode.data = company[3]
        edit_organization_form.companytype.choices = [(g.company_type_id, g.description) for g in company_types]
    
    #select(Companies).filter_by(company_id=int(id))
    #company = db.session.execute(statement, {'parm1' : comp_id}).fetchone()
    if edit_organization_form.is_submitted and request.method == 'POST':
        new_name = edit_organization_form.companyname.data
        new_desc = edit_organization_form.companydesc.data
        new_code = edit_organization_form.companycode.data
        new_type = edit_organization_form.companytype.data

        statement = 'UPDATE companies SET name = :parm1, description = :parm2, code = :parm3, company_type_id = :parm4 where company_id = :parm5'
        company = db.session.execute(statement, {'parm1' : new_name, 'parm2' : new_desc, 'parm3' : new_code, 'parm4' : new_type, 'parm5': comp_id, })
        db.session.commit()
        print("POST ...",edit_organization_form.data)
        return redirect(url_for('organizations_blueprint.allcompanies'))

    print("El form >>> ", edit_organization_form.data)
    return render_template('organizations/company_modal.html', form=edit_organization_form, company_types=company_types)
