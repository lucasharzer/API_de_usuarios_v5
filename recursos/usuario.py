from flask_restful import Resource, reqparse
from modelos.usuario import ModeloUsuario
from modelos.rede import ModeloRede
from recursos.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3

# path /usuarios?cidade=Rio de Janeiro&idade_min=4
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('idade_min', type=float)
path_params.add_argument('idade_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Usuarios(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        usuarios = []
        for linha in resultado:
            usuarios.append({
                'usuario_id': linha[0],
                'nome': linha[1],
                'idade': linha[2],
                'cidade': linha[3],
                'rede_id': linha[4]
            })

        return {'usuarios': usuarios} 


class Usuario(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="the field 'nome' is required")
    argumentos.add_argument('idade', type=float, required=True, help="the field 'idade' is required")
    argumentos.add_argument('cidade')
    argumentos.add_argument('rede_id', type=int, required=True, help="Every user need to be linked with network.")

    def get(self, usuario_id):
        usuario = ModeloUsuario.encontrar_usuario(usuario_id)
        if usuario:
            return usuario.json()
        return {'message': 'User not found.'}, 404
    
    @jwt_required()
    def post(self, usuario_id):
        if ModeloUsuario.encontrar_usuario(usuario_id):
            return {"message": "User id '{}' already exists.".format(usuario_id)}, 400 

        dados = Usuario.argumentos.parse_args()
        usuario = ModeloUsuario(usuario_id, **dados)

        if not ModeloRede.encontrar_pelo_id(dados['rede_id']):
            return {'message': 'The user must be associaded to a valid network id.'}, 400
        try:
            usuario.salvar_usuario()
        except:
            return {"message": "An internal error ocurred trying to save user."}, 500
        return usuario.json()

    @jwt_required()
    def put(self, usuario_id):
        dados = Usuario.argumentos.parse_args()
        usuario_encontrado = ModeloUsuario.encontrar_usuario(usuario_id)
        if usuario_encontrado:
            usuario_encontrado.atualizar_usuario(**dados)
            usuario_encontrado.salvar_usuario()
            return usuario_encontrado.json(), 200 
        usuario = ModeloUsuario(usuario_id, **dados)
        try:
            usuario.salvar_usuario()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
        return usuario.json(), 201 

    @jwt_required()
    def delete(self, usuario_id):
        usuario = ModeloUsuario.encontrar_usuario(usuario_id)
        if usuario:
            try:
                usuario.deletar_usuario()
            except:
                return {'message': 'An error occured trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404