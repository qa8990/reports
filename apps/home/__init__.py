# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

#print("estoy en blueprint home/S__init__ ")
blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)
