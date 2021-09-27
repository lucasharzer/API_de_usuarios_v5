from flask_restful import Resource, reqparse
from modelos.conta import ModeloConta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)

class Conta(Resource):

    def get(self, conta_id):
        conta = ModeloConta.encontrar_conta(conta_id)
        if conta:
            return conta.json()
        return {'message': 'Account not found.'}, 404 

    @jwt_required()
    def delete(self, conta_id):
        conta = ModeloConta.encontrar_conta(conta_id)
        if conta:
            conta.deletar_conta()
            return {'message': 'Account deleted.'}
        return {'message': 'Account not found.'}, 404

class RegistrarConta(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        if ModeloConta.encontrar_pelo_email(dados['email']):
            return {"message": "The email {} already exists.".format(dados['email'])}, 400

        if ModeloConta.encontrar_pelo_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}
        
        conta = ModeloConta(**dados)
        conta.ativado = False
        try:
            conta.salvar_conta()
            conta.enviar_confirmacao_por_email()
        except:
            conta.deletar_conta()
            traceback.print_exc()
            return {"message": "An internal server error has occured."}, 500
        return {'message': 'Account created successfully!'}, 201 

class LoginConta(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        conta = ModeloConta.encontrar_pelo_login(dados['login'])

        if conta and safe_str_cmp(conta.senha, dados['senha']):
            if conta.ativado:
                token_de_acesso = create_access_token(identity=conta.conta_id)
                return {'acess_token': token_de_acesso}, 200
            return {"message": "Account not confirmed."}, 400
        return {'message': 'The account or password is incorrect.'}, 401 


class LogoutConta(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'massage': 'Logged out successfully!'}, 200

class ConfirmarConta(Resource):
    @classmethod
    def get(cls, conta_id):
        conta = ModeloConta.encontrar_conta(conta_id)

        if not conta:
            return {"message": "Account id '{}' not found.".format(conta_id)}, 404

        conta.ativado = True
        conta.salvar_conta()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('account_confirm.html', email=conta.email, conta=conta.login), 200, headers)