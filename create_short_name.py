import string

from application import *

vs = db.session.query(models.Video).all()

def mk_short(s):
    return s[:2] + ''.join([c for c in s if c in string.digits])

for v in vs:
    v.short_name = mk_short(v.name)

db.session.commit()
