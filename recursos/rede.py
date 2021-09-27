from flask_restful import Resource
from modelos.rede import ModeloRede

class Redes(Resource):
    def get(self):
        return {'redes': [rede.json() for rede in ModeloRede.query.all()]}

class Rede(Resource):
    def get(self, url):
        rede = ModeloRede.encontrar_rede(url)
        if rede:
            return rede.json()
        return {'message': 'Network not found.'}, 404 # not found

    def post(self, url):
        if ModeloRede.encontrar_rede(url):
            return {"message": "The network '{}' already exists."}, 400 # bad request
        rede = ModeloRede(url)
        try:
            rede.salvar_rede()
        except:
            return {'message': 'An internal error ocurred trying to create a new network.'}, 500
        return rede.json()

    def delete(self, url):
        rede = ModeloRede.encontrar_rede(url)
        if rede:
            rede.deletar_rede()
            return {'message': 'Network deleted.'}
        return {'message': 'Network not found.'}, 404