from flask import render_template, redirect, request, url_for
from flask_sqlalchemy import Pagination
from flask_modals import render_template_modal, response
from apps.masterplan import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.masterplan.forms import MasterPlanForm
#from apps.masterplan.models import MasterPlan
from sql_app.models import MasterPlan
from apps.dbManager import  create_new_account, clean_master_plan, upload_master_plan
from apps.organizations.util import get_json_data
import datetime

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates 
from starlette.middleware.wsgi import WSGIMiddleware

API_GET = "GET"
API_POST = "POST"
API_PUT = "PUT"


@blueprint.route('/masterplans', methods=['GET'])
def masterplan_2():
    json_data = {}
    limit = 10
    page = request.args.get('page', 1, type=int)
    response = get_json_data(API_GET, request.path, page, limit, json_data)

    if response :
        myList = response['items']
        totalList = response['total']
        pagination = Pagination( None, page=page, per_page=10, total=totalList, items=myList)
        return render_template('masterplan/masterplan.html', pagination=pagination, page=page, total=totalList)
    

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

@blueprint.route('/account/<id>', methods=['GET', 'POST'])    
def edit_account(id):
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