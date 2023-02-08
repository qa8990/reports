from flask import Flask, render_template, redirect, request, url_for, jsonify, Response
from flask_modals import render_template_modal, response
from apps.organizations import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.organizations.forms import CreateOrganizationForm, OrganizationForm
from apps.organizations.models import Companies, CompaniesTypes
from apps.dbManager import create_new_company

from pathlib import Path

from apps import create_app
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates 
from starlette.middleware.wsgi import WSGIMiddleware

from apps.organizations.util import get_current_date_time, get_json_data

ACTIVO = 1

templates = Jinja2Templates(directory="templates")
ALL_PARMS = "?skip=0&limit=100"

# Organization

@blueprint.route('/companies', methods=['GET'])
def companies():
    print('/Allcompanies ', request.path)

    response = get_json_data(request.path, ALL_PARMS)

    if response :
        return render_template('organizations/companies.html', company=response)
    
@blueprint.route('/allcompanies2', methods=['GET'])
def allcompanies2():
    print('@@@ ### Allcompanies route ####  @@@')
      
    # Other style
    #company = db.session.execute(select(Companies.company_id, Companies.name, Companies.description, CompaniesTypes.description, CompaniesTypes.image, Companies.created_at).join(CompaniesTypes.type)).all()
    #company_obj = Companies.query.filter_by(status_id = ACTIVO).fetchall()
    company_obj = Companies.get_all()
    print('#2', company_obj, type(company_obj))  #devuelve un objeto Companies
    print('@@@ ### Allcompanies route ####  @@@', company_obj, type(company_obj))

    # Check the password
    if company_obj :
        return render_template('organizations/companies.html', company=company_obj)

@blueprint.route('/editcompanies', methods=['GET'])
def companies():
    print('/Allcompanies ', request.path)

    response = get_json_data(request.path, ALL_PARMS)

    if response :
        return render_template('organizations/companies.html', company=response)
    

@blueprint.route('/edit_company/<id>', methods=['GET', 'POST'])
def edit_company(id):

    print('En el EDIT_COMPANY')
    form = OrganizationForm(request.form)
    company_obj = Companies()
   
    #if request.method == 'GET':
    print('Select(companies --->', id)
    #company = db.session.execute(select(Companies.company_id, Companies.name, Companies.description).where(Companies.company_id == id)).all()
    company = db.session.execute(db.Query(Companies)).fetchall()
    company_obj = Companies.query.filter_by(company_id = id).one()
    print('#1', company, type(company))
    print('#2', company_obj.name, type(company_obj))  #devuelve un objeto Companies
    form = OrganizationForm(company_obj.name)
    form.companyname.data = company[1]
    form.companydesc.data = company[2]
        #form.companycode.data = company[3]
        #form.companytype.choices = [(g.company_type_id, g.description) for g in company_types]
        #return redirect(url_for('organizations_blueprint.allcompanies'), company=company_obj, form=form)
    render_template('organizations/modal.html', form=form)

@blueprint.route('/edit_company2/<id>', methods=['GET', 'POST'])    
def edit_company2(id):
    form = OrganizationForm()
    if request.method == 'GET':
        company = Companies.get_company_byId(id)
        companyTypes = CompaniesTypes.get_all_company_types()
        form.name.data = company[0][1]
        form.description.data = company[0][2]
        form.code.data = company[0][6]
        form.company_type_id.choices = [(g.company_type_id, g.description) for g in companyTypes]
        print('edit-company2', form.data)
        return render_template('organizations/organization.html',  id=id, form=form)

    if form.is_submitted and request.method == 'POST':
        company = Companies.update_company_byId(form, id)
        return redirect(url_for('organizations_blueprint.allcompanies'))

@blueprint.route('/add_company', methods=['GET', 'POST'])    
def add_company():
    form = CreateOrganizationForm(request.form)
    companyTypes = CompaniesTypes.get_all_company_types()
    if request.method == 'GET':
        company = Companies()
        companyTypes = CompaniesTypes.get_all_company_types()
        form.company_type_id.choices = [(g.company_type_id, g.description) for g in companyTypes]
        print('edit-company2', form.data)
        return render_template('organizations/organization.html',  form=form)

    if form.is_submitted and request.method == 'POST':
        company = Companies(**request.form)
        #Companies(
        #    companyname = request.form["companyname"],
        #    companydesc = request.form["companydesc"],
        #    companycode = request.form["companycode"],
        #    companytype = request.form["companytype"]
        #)
        print("-----------------compnay adding &&&&&&&&&&&&&&&& ------------------------------")
        print( request.form)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(company)
        print("-----------------compnay adding &&&&&&&&&&&&&&&& ------------------------------")
        new_company = create_new_company(company)
        return redirect(url_for('organizations_blueprint.allcompanies'))       

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
        companyTypes = CompaniesTypes.get_all_company_types()
        
        #company_obj = Companies(company)
        print(companyTypes)
        edit_organization_form.companyname.data = company[1]
        edit_organization_form.companydesc.data = company[2]
        edit_organization_form.companycode.data = company[3]
        edit_organization_form.companytype.choices = [(g.company_type_id, g.description) for g in companyTypes]
    
    #select(Companies).filter_by(company_id=int(id))
    #company = db.session.execute(statement, {'parm1' : comp_id}).fetchone()
    if edit_organization_form.is_submitted and request.method == 'POST':
        new_name = edit_organization_form.companyname.data
        new_desc = edit_organization_form.companydesc.data
        new_code = edit_organization_form.companycode.data
        new_type = edit_organization_form.companytype.data

        #statement = 'UPDATE companies SET name = :parm1, description = :parm2, code = :parm3, company_type_id = :parm4 where company_id = :parm5'
        #company = db.session.execute(statement, {'parm1' : new_name, 'parm2' : new_desc, 'parm3' : new_code, 'parm4' : new_type, 'parm5': comp_id, })
        #db.session.commit()
        
        print("POST ...",edit_organization_form.data)
        return redirect(url_for('organizations_blueprint.allcompanies'))

    print("El form >>> ", edit_organization_form.data)
    return render_template('organizations/company_modal.html', form=edit_organization_form, company_types=companyTypes)
    #render_template('organizations/edit_company.html', form=edit_organization_form, company_types=company_types)
    

@blueprint.route('/addcompany', methods=['GET', 'POST'])
def addcompany():
    add_organization_form = CreateOrganizationForm(request.form)
    print("Estoy en add company -->")
    #company_form = OrganizationForm()

    company_types = db.session.execute(select(CompaniesTypes.company_type_id, CompaniesTypes.code, CompaniesTypes.description).where(CompaniesTypes.status_id == 1)).all()
    #add_organization_form = CreateOrganizationForm(request.form)
    print('request ====0 // ', add_organization_form.data)

    if add_organization_form.is_submitted and request.method == 'POST':
        print('request ==== 1// ', add_organization_form.data)

        statement = 'INSERT INTO companies SET name = :parm1, description = :parm2, code = :parm3, company_type_id = :parm4'
        print("LA data es $$$$$ ", add_organization_form.companytype.data)
        #company = Companies()
        print('Request ** - en add company []',**request.form)
        company2 = Companies(**request.form)
        print("Company 22 ===->>",company2)
        #company.company_id = add_organization_form.companycode.data
        #company.name = add_organization_form.companyname.data
        #company.description = add_organization_form.companydesc.data
        #company.code = add_organization_form.companycode.data
        #company.company_type_id = add_organization_form.companytype.data
        #company.status_id = 1
        
        #print(company)
        #company = db.session.execute(statement, {'parm1' : add_organization_form.companyname.data, 'parm2' : add_organization_form.companydesc.data, 'parm3' : add_organization_form.companycode.data, 'parm4' : add_organization_form.companytype.data })
        #db.session.add(company2)
        #db.session.commit()
        print("POST ...",add_organization_form.data)
        return redirect(url_for('organizations_blueprint.allcompanies'))
    else:
        #add_organization_form.companytype = company_types
        add_organization_form.companytype.choices = [(g.company_type_id, g.description) for g in company_types]
        print('En el else de ADD companies ', add_organization_form, company_types)
        return render_template('organizations/company_modal create.html', form=add_organization_form, company_types=company_types)
    #print("El form >>> ", add_organization_form.data)
    #return render_template('organizations/company_modal create.html', form=add_organization_form, company_types=company_types)