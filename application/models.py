from application import db

class Sessao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    data = db.Column(db.Date())

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    vereador = db.relationship('Vereador', backref='partido', lazy='dynamic')

class Vereador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    idparlamentar = db.Column(db.Integer)
    partido_id = db.Column(db.Integer, db.ForeignKey('partido.id'))

class Votacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votacaoid = db.Column(db.Integer)
    sessao_id = db.Column(db.Integer, db.ForeignKey('sessao.id'))
    tipo = db.Column(db.Text)
    materia = db.Column(db.Text)
    ementa = db.Column(db.Text)
    resultado = db.Column(db.Text)
    presentes = db.Column(db.Integer)
    sim = db.Column(db.Integer)
    nao = db.Column(db.Integer)
    abstencao = db.Column(db.Integer)
    branco = db.Column(db.Integer)
    notas_rodape = db.Column(db.Text)

class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votacao_id = db.Column(db.Integer, db.ForeignKey('votacao.id'))
    vereador_id = db.Column(db.Integer, db.ForeignKey('vereador.id'))
    valor = db.Column(db.Text)

##
# Create your own models here and they will be imported automaticaly. or
# use a model per blueprint.

##
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(80), unique=True)
#     password = db.Column(db.String(80))

#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.password = password

#     def __repr__(self):
#         return '<User %r>' % (self.username)

##
# class Log(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     time = db.Column(db.DateTime)
#     hostname = db.Column(db.String(20))
#     flagger = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref='log', lazy='dynamic')

#     def __init__(self, time, uptime, hostname, flagger, user_id):
#         self.returns = 0
#         self.errors = 0
#         self.time = time
#         self.hostname = hostname
#         self.flagger = flagger
#         self.user_id = user_id

#     def __repr__(self):
#         return '<Log %r>' % (self.hostname)
