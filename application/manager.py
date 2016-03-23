# -*- coding: utf-8 -*-

from application import app
from flask import render_template
from application.models import *
from flask_restplus import Api, Resource, fields
from flask.ext.restplus.reqparse import RequestParser
from flask.ext.restplus.inputs import date
import application.script_creator as sc
import json

api = Api(app, version='1.0', title=u'Mobiliário Urbano API')
ns = api.namespace('elesvotam', description=u'Mobiliário Urbano Operations')

video_parser = RequestParser()
video_parser.add_argument('video_id', type=int)

video_fields = {'id': fields.Integer(),
                'name': fields.String(),
                'duration': fields.Float(),
                'high_def': fields.String(),
                'standard_def_big': fields.String(),
                'standard_def_small': fields.String(),
                }

video_model = api.model('Video', video_fields)

@app.route('/roteiro')
def roteiro():
    roteiro = sc.cria_roteiro()
    return json.dumps(roteiro)

@app.route('/index/')
def index():
    return render_template('info/index.html', title='Flask-Bootstrap')

