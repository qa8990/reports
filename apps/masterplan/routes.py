from flask import render_template, redirect, request, url_for
from flask_modals import render_template_modal, response
from apps.masterplan import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.masterplan.forms import MasterPlanForm
from apps.masterplan.models import MasterPlan
from apps.dbManager import create_new_company, create_new_account, clean_master_plan, upload_master_plan


@blueprint.route('/')
def route_default():
    print('Here')
    return redirect(url_for('organizations_blueprint.allcompanies'))


# Accounts

@blueprint.route('/masterplan', methods=['GET'])
def masterplan():
    print('----------------------- ### Master Plan route ####  ----------------')
    #print("page nbr :", page_nbr, type(int(page_nbr)))
    #page_nbr= int(page_nbr)
    page = request.args.get('page', 1, type=int)
    pagination = MasterPlan.get_all(page)

    # Check the password
    if pagination :
        return render_template('masterplan/masterplan.html', pagination=pagination, page = page)


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