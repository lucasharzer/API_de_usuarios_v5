from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'sandboxe7916b0645934d60ac2907a0c01fffb2.mailgun.org'
MAILGUN_API_KEY = 'd902c8f2b5c406571c205e6e91a5fa52-90346a2d-e9350d51'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@restapi.com'

class ModeloConta(banco.Model):
    __tablename__ = 'contas'

    conta_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def enviar_confirmacao_por_email(self):
        # https://127.0.0.1:5000/confirmacao/{conta_id}
        link = request.url_root[:-1] + url_for('confirmarconta', conta_id=self.conta_id)
        # slicing de strings
        return post(
            'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
            auth=('api', MAILGUN_API_KEY),
            data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
			'to': self.email,
			'subject': 'Confirmação de Cadastro',
			'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
            'html': '<html><p>\
            Confirme seu cadastro clicando no link a seguir: <a href="{}">CONFIRMAR EMAIL</a>\
            </p></html>'.format(link)
            }
        )

    def json(self):
        return {
            'conta_id': self.conta_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado,
            }

    @classmethod
    def encontrar_conta(cls, conta_id):
        conta = cls.query.filter_by(conta_id=conta_id).first()
        if conta:
            return conta
        return None

    @classmethod
    def encontrar_pelo_login(cls, login):
        conta = cls.query.filter_by(login=login).first()
        if conta:
            return conta
        return None

    @classmethod
    def encontrar_pelo_email(cls, email):
        conta = cls.query.filter_by(email=email).first()
        if conta:
            return conta
        return None

    def salvar_conta(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_conta(self):
        banco.session.delete(self)
        banco.session.commit()