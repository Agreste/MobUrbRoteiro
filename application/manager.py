# -*- coding: utf-8 -*-

from application import app
from flask import render_template
from application.models import *
from flask_restplus import Api, Resource, fields
from flask.ext.restplus.reqparse import RequestParser
from flask.ext.restplus.inputs import date
import application.script_creator2 as sc
import json
import random

api = Api(app, version='1.0', title=u'Mobiliário Urbano API', doc='/api')
ns = api.namespace('MobUrb', description=u'Mobiliário Urbano Operations')

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
@app.route('/roteiro/<slug>')
def roteiro(slug=None):
    if not slug:
        cortes = random.randint(7, 12)
        roteiro = sc.cria_roteiro(numero_maximo = cortes)
    else:
        roteiro = sc.decode_slug(slug)
    return json.dumps(roteiro)

