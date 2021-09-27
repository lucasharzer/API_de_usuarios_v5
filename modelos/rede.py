from sql_alchemy import banco

class ModeloRede(banco.Model):
    __tablename__ = 'redes'

    rede_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    usuarios = banco.relationship('ModeloUsuario')

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'rede_id': self.rede_id,
            'url': self.url,
            'usuarios': [usuario.json() for usuario in self.usuarios]
        }

    @classmethod
    def encontrar_rede(cls, url):
        rede = cls.query.filter_by(url=url).first()
        if rede:
            return rede
        return None

    @classmethod
    def encontrar_pelo_id(cls, rede_id):
        rede = cls.query.filter_by(rede_id=rede_id).first()
        if rede:
            return rede
        return None

    def salvar_rede(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_rede(self):
        [usuario.deletar_usuario() for usuario in self.usuarios]
        banco.session.delete(self)
        banco.session.commit()