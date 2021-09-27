from sql_alchemy import banco

class ModeloUsuario(banco.Model):
    __tablename__ = 'usuarios'

    usuario_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80)) 
    idade = banco.Column(banco.Float(precision=1)) 
    cidade = banco.Column(banco.String(40))
    rede_id = banco.Column(banco.Integer, banco.ForeignKey('redes.rede_id'))

    def __init__(self, usuario_id, nome, idade, cidade, rede_id):
        self.usuario_id = usuario_id
        self.nome = nome
        self.idade = idade
        self.cidade = cidade
        self.rede_id = rede_id

    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'nome': self.nome,
            'idade': self.idade,
            'cidade': self.cidade,
            'rede_id': self.rede_id
        }

    @classmethod
    def encontrar_usuario(cls, usuario_id):
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()
        if usuario:
            return usuario
        return None

    def salvar_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_usuario(self, nome, idade, cidade, rede_id):
        self.nome = nome
        self.idade = idade
        self.cidade = cidade
        self.rede_id = rede_id

    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
