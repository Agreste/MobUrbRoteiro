from application import db
from sqlalchemy.orm import relationship

class Sessao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    data = db.Column(db.Date())
    votacao = relationship("Votacao", back_populates="sessao")

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    vereador = db.relationship('Vereador', backref='partido', lazy='dynamic')

class Vereador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    idparlamentar = db.Column(db.Integer)
    partido_id = db.Column(db.Integer, db.ForeignKey('partido.id'))
    votos = relationship("Voto", back_populates="vereador")

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
    votos = relationship("Voto", back_populates="votacao")
    sessao = relationship("Sessao", back_populates="votacao")

class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votacao_id = db.Column(db.Integer, db.ForeignKey('votacao.id'))
    vereador_id = db.Column(db.Integer, db.ForeignKey('vereador.id'))
    valor = db.Column(db.Text)
    vereador = relationship("Vereador", back_populates="votos")
    votacao = relationship("Votacao", back_populates="votos")
