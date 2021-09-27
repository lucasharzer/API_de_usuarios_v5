from flask import Flask, jsonify
from flask_restful import Api
from recursos.usuario import Usuarios, Usuario
from recursos.conta import Conta, RegistrarConta, LoginConta, LogoutConta, ConfirmarConta
from recursos.rede import Rede, Redes
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401 

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuarios/<string:usuario_id>')
api.add_resource(Conta, '/contas/<int:conta_id>')
api.add_resource(RegistrarConta, '/cadastro')
api.add_resource(LoginConta, '/login')
api.add_resource(LogoutConta, '/logout')
api.add_resource(Redes, '/redes')
api.add_resource(Rede, '/redes/<string:url>')
api.add_resource(ConfirmarConta, '/confirmacao/<int:conta_id>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

# http://127.0.0.1:5000/ 