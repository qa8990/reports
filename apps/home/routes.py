# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.organizations.util import get_last_company_added
from apps.organizations.models import Companies
from apps import db


@blueprint.route('/index')
@login_required
def index():
    last_data = Companies.get_last_company_added()
    print(last_data)

    return render_template('home/index.html', segment='index', company=last_data)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    last_data = Companies.get_last_company_added()
    print(last_data)
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:
        
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
