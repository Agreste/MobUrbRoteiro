from flask import Flask, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields
from flask.ext.restplus.reqparse import RequestParser
from flask.ext.cors import CORS, cross_origin

# Create the app and configuration
# Read the configuration file
app = Flask(__name__)
cors = CORS(app)
app.config.from_object('application.default_settings')
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)


# Connect to database with sqlalchemy.
db = SQLAlchemy(app)

# 404 page not found "route"
@app.errorhandler(404)
def not_found(error):
    title = "404 Page not found"
    return render_template('404.html', title=title), 404


# 500 server error "route"
@app.errorhandler(500)
def server_error(error):
    title = "500 Server Error"
    db.session.rollback()
    return render_template('500.html', title=title), 500

@app.route('/mais')
def mais():
    return render_template('mais.html'), 200

@app.route('/sobre')
def sobre():
    return render_template('sobre.html'), 200

@app.route('/creditos')
def creditos():
    return render_template('creditos.html'), 200

@app.route('/')
@app.route('/<slug>')
def index(slug=None):
    return render_template('video.html'), 200

import application.manager
