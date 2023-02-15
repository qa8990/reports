from flask import render_template, redirect, request, url_for
from flask_modals import render_template_modal, response
from apps.masterplan import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.masterplan.forms import MasterPlanForm
#from apps.masterplan.models import MasterPlan
from sql_app.models import MasterPlan
from apps.dbManager import  create_new_account, clean_master_plan, upload_master_plan
from apps.organizations.util import get_json_data

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates 
from starlette.middleware.wsgi import WSGIMiddleware

API_GET = "GET"
API_POST = "POST"
API_PUT = "PUT"
#ALL_PARMS = "?skip=0&limit=100"

# Accounts
#@blueprint.route('/masterplan', methods=['GET'])
# def get_masterplan():
#    print('----------------------- ### Master Plan route ####  ----------------')
#    json_data = {}
#    page = request.args.get('page', 1, type=int)
#    response = get_json_data(API_GET, request.path, ALL_PARMS, json_data)
#    print("en el ")
#    if response :
#        print("estoy en el if response ")
#        return render_template('masterplan/masterplan.html', pagination=response, page = page)

@blueprint.route('/masterplans', methods=['GET'])
def masterplan_2():
    print('----------------------- ### Master Plan 2 route ####  ----------------')
    #print("page nbr :", page_nbr, type(int(page_nbr)))
    #page_nbr= int(page_nbr)

    # NEW
    json_data = {}
    limit = 20
    page = request.args.get('page', 1, type=int)
    response = get_json_data(API_GET, request.path, page, limit, json_data)
    print("en el -- page", page)
    if response :
        print("estoy en el if response ", response)
        return render_template('masterplan/masterplan.html', pagination=response, page = page)
    
    # end NEW
    #--------
    # OLD
    # page = request.args.get('page', 1, type=int)
    # pagination = MasterPlan.get_all(page)

    # Check the password
    #if pagination :
    #    return render_template('masterplan/masterplan.html', pagination=pagination, page = page)
    # OLD

@blueprint.route('/addaccount', methods=['GET', 'POST'])
def addaccount():
    print('----------------------- ### Master Plan route ####  ----------------')
      
    form = MasterPlanForm(request.form)

    # Check the password
    if request.method == 'GET':
        plan = MasterPlan()
        #companyTypes = CompaniesTypes.get_all_company_types()
        #form.company_type_id.choices = [(g.company_type_id, g.description) for g in companyTypes]
        print('edit-company2', form.data)
        return render_template('masterplan/accounting.html',  form=form)

    if request.method == 'POST':
        account = MasterPlan(**request.form)
        #companyTypes = CompaniesTypes.get_all_company_types()
        #form.company_type_id.choices = [(g.company_type_id, g.description) for g in companyTypes]
        new_account = create_new_account(account)
        return redirect(url_for('masterplan_blueprint.masterplan'))    


@blueprint.route('/viewplan', methods=['GET'])
def viewplan():
    print('----------------------- ### Master Plan route ####  ----------------')
    #print("page nbr :", page_nbr, type(int(page_nbr)))
    #page_nbr= int(page_nbr)
    #upload_master_plan()
    clean_master_plan()  
    upload_master_plan()
    # Check the password
    return  redirect(url_for('masterplan_blueprint.masterplan'))    

@blueprint.route('/editaccounting/<id>', methods=['GET', 'POST'])    
def editaccounting(id):
    form = MasterPlanForm()
    if request.method == 'GET':
        plan = MasterPlan.get_account_byId(id)
        form.account_number.data = plan[0][1]
        form.account_name.data = plan[0][2]
        print("plan --", plan)
        print('edit-plan', form.data, type(form))
        return render_template('masterplan/accounting.html',  id=id, form=form)

    if form.is_submitted and request.method == 'POST':
        plan = MasterPlan.update_account_byId(form, id)
        return redirect(url_for('masterplan_blueprint.masterplan'))