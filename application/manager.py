from application import app
from flask import render_template
from application.models import *
from flask_restplus import Api, Resource, fields
from flask.ext.restplus.reqparse import RequestParser
from flask.ext.restplus.inputs import date

api = Api(app, version='1.0', title='ElesVotam API')
ns = api.namespace('elesvotam', description='ElesVotam operations')

votacao_parser = RequestParser()
votacao_parser.add_argument('votacaoid', type=int)

votacao_fields = {'votacaoid': fields.Integer(),
                  'sessao_id': fields.Integer(),
                  'tipo': fields.String(),
                  'materia': fields.String(),
                  'ementa': fields.String(),
                  'resultado': fields.String(),
                  'presentes': fields.String(),
                  'sim': fields.Integer(),
                  'nao': fields.Integer(),
                  'abstencao': fields.Integer(),
                  'branco': fields.Integer(),
                  'notas_rodape': fields.String(),
                  }

votacao_model = api.model('Votacao', votacao_fields)

@ns.route('/votacao')
class ElesVotamVotacaosApi(Resource):
    @api.doc(parser=votacao_parser)
    @api.marshal_with(votacao_model)
    def get(self):
        args = votacao_parser.parse_args()
        votacaoid = args['votacaoid']
        votacao = db.session.query(Votacao).filter(Votacao.votacaoid == votacaoid).one()
        return votacao

sessao_parser = RequestParser()
sessao_parser.add_argument('sessaoid', type=int)
sessao_parser.add_argument('data', type=date)

sessao_fields = {'id': fields.Integer(),
                 'nome': fields.String(),
                 'data': fields.Date(),
                 'votacoes': fields.Nested(votacao_model)
                  }

sessao_model = api.model('sessao', sessao_fields)

@ns.route('/sessao')
class ElesVotamSessaosApi(Resource):
    @api.doc(parser=sessao_parser)
    @api.marshal_with(sessao_model)
    def get(self):
        args = sessao_parser.parse_args()
        sessaoid = args['sessaoid']
        sessao_date = args['data']
        if not sessao_date:
            sessao = db.session.query(Sessao).filter(Sessao.id == sessaoid).one()
            votacoes = db.session.query(Votacao).filter(Votacao.sessao_id == sessao.id).all()
            sessao.votacoes = votacoes

        else:
            sessao_date = sessao_date.strftime('%Y-%m-%d')
            sessao = db.session.query(Sessao).filter(Sessao.data == sessao_date).all()

            for i,s in enumerate(sessao):
                votacoes = db.session.query(Votacao).filter(Votacao.sessao_id == s.id).all()
                sessao[i].votacoes = votacoes

        return sessao


partido_fields = {'id': fields.Integer(),
                  'nome': fields.String(),
                  }

partido_model = api.model('partido', partido_fields)

@ns.route('/partidos')
class ElesVotamPartidosApi(Resource):
    @api.marshal_with(partido_model)
    def get(self):
        partidos = db.session.query(Partido).all()

        return partidos

partido_parser = RequestParser()
partido_parser.add_argument('nome', type=str)

vereador_fields = {'id': fields.Integer(),
                  'nome': fields.String(),
                  'idparlamentar': fields.String()
                  }

vereador_model = api.model('vereador', vereador_fields)

@ns.route('/partidoVereadores')
class ElesVotamPartidoVereadoresApi(Resource):
    @api.doc(parser=partido_parser)
    @api.marshal_with(vereador_model)
    def get(self):
        args = partido_parser.parse_args()
        partido_nome = args['nome']

        partido = db.session.query(Partido).filter(Partido.nome == partido_nome).one()
        vereadores = db.session.query(Vereador).filter(Vereador.partido_id == partido.id).all()

        return vereadores

votacao_votos_parser = RequestParser()
votacao_votos_parser.add_argument('votacao_id', type=int)

voto_fields = {'id': fields.Integer(),
               'vereador': fields.Nested(vereador_model),
               'valor': fields.String()
}

voto_model = api.model('voto', voto_fields)

@ns.route('/votacaoVotos')
class ElesVotamVotacaoVotosApi(Resource):
    @api.doc(parser=votacao_votos_parser)
    @api.marshal_with(voto_model)
    def get(self):
        args = votacao_votos_parser.parse_args()
        votacao_id = args['votacao_id']
        votos = db.session.query(Voto).filter(Voto.votacao_id == votacao_id).all()

        return votos


@app.route('/')
@app.route('/index/')
def index():
    return render_template('info/index.html', title='Flask-Bootstrap')


@app.route('/hello/<username>/')
def hello_username(username):
    return render_template('info/hello.html', title="Flask-Bootstrap, Hi %s"
                            % (username), username=username)
