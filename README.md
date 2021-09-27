# Descrição

Rest API com Python, Flask, com banco de dados SQLAlchemy, JWT que disponibiliza um token de acesso e confirmação de conta por email. Possui os métodos GET (listar todas contas), DELETE (deletar uma conta), POST (cadastro de uma conta inserindo os dados: login, senha e email), GET (confirmação por email - ativa a conta), POST (login da conta - libera o token), POST (loggout da conta - requer o token), GET (listar todos os usuários e listar usuários por id), POST (cadastrar usuario inserindo os dados: usuario_id, nome, idade, cidade e rede_id - requer o token), PUT (atualizar usuários por id - requer o token), DELETE (deletar usuários por id - requer o token), GET (listar redes e listar redes pela URL), POST (criar redes inserindo a URL - requer o token) e DELETE (deletar a rede pela URL - requer o token).

Obs: É possível criar contas através do cadastro, dentro de uma conta é possível criar várias redes e dentro de uma rede é possível criar vários usuarios.

# Comandos no terminal para configuração

```bash
python setup.py develop
```

# Rodando a aplicação

```bash
python principal.py
```

# Teste no Postman

- Conta desativada:

<span align="center">
    <img src="https://user-images.githubusercontent.com/85804895/134938815-ab8f12e6-e2aa-4afc-86ce-08d122eefd49.png", width=900>
</span>

- Pedir confirmação:

<span align="center">
    <img src="https://user-images.githubusercontent.com/85804895/134939123-07b47f49-08ac-40a3-ac9f-c727306a4f6d.png", width=900>
</span>

- Checar emails e confirmar:

<span align="center">
    <img src="https://user-images.githubusercontent.com/85804895/134939323-91040008-6c5f-4b0b-b268-a0d9fed380be.png", width=900>
</span>

<span align="center">
    <img src="https://user-images.githubusercontent.com/85804895/134939557-3a93b486-f641-4546-b4af-fc929819c143.png", width=900>
</span>

- Conta ativada:

<span align="center">
    <img src="https://user-images.githubusercontent.com/85804895/134939667-6fc5eaf6-4884-4bea-a753-84ae92408b22.png", width=900>
</span>
