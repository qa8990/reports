from flask import render_template, redirect, request, url_for
from flask_modals import render_template_modal, response
from apps.reports import blueprint
from apps import db, props, sql_scripts
from sqlalchemy import select
from apps.reports.forms import ReportsForm
from apps.reports.models import ReportsForma
#from apps.dbManager import create_new_company, create_new_account, clean_master_plan, upload_master_plan


@blueprint.route('/')
def route_default():
    print('Here')
    return redirect(url_for('masterplan_blueprint.masterplan'))


# Reports
@blueprint.route('/reports')
def reports():
    print('Here')
    forma = ReportsForma.get_all()
    return render_template('reports/reports.html', forma=forma)
