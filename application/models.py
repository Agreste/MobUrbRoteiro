from application import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    duration = db.Column(db.Integer)
    high_def = db.Column(db.Text)
    standard_def_small = db.Column(db.Text)
    standard_def_big = db.Column(db.Text)
