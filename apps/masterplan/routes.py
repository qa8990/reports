from flask import render_template, redirect, request, url_for
from flask_modals import render_template_modal, response
from apps.masterplan import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.masterplan.forms import MasterPlanForm
from apps.masterplan.models import MasterPlan
from apps.dbManager import create_new_company, create_new_account

@blueprint.route('/')
def route_default():
    print('Here')
    return redirect(url_for('organizations_blueprint.allcompanies'))


# Accounts

@blueprint.route('/masterplan', methods=['GET'])
def masterplan():
    print('----------------------- ### Master Plan route ####  ----------------')
      
    account = MasterPlan.get_all()

    # Check the password
    if account :
        return render_template('masterplan/masterplan.html', masterplan=account)


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