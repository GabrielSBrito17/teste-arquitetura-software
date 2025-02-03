# API RESTful com Arquitetura MVC

Este projeto é uma API RESTful desenvolvida em Python utilizando o framework Flask. A aplicação segue o padrão arquitetural MVC (Model-View-Controller) e implementa operações CRUD básicas para um domínio de Clientes.

## 1. Estrutura do Projeto

A estrutura de pastas segue o padrão MVC e é organizada da seguinte forma:

```
api_mvc/
│
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   └── cliente_controller.py
│   ├── models/
│   │   └── cliente_model.py
│   ├── services/
│   │   └── cliente_service.py
│   └── views/
│       └── cliente_view.py
│
├── config/
│   └── config.py
│
├── tests/
│   └── test_cliente.py
│
├── requirements.txt
├── run.py
└── README.md
```

## 2. Descrição dos Componentes

- **`app/controllers/`**: Contém os controladores que gerenciam as requisições e respostas da API.
- **`app/models/`**: Contém as entidades (modelos) que representam os dados.
- **`app/services/`**: Contém a lógica de negócio e interação com os dados.
- **`app/views/`**: Contém as funções que formatam os dados para a resposta da API.
- **`config/`**: Contém configurações da aplicação, como conexão com banco de dados.
- **`tests/`**: Contém testes unitários e de integração.
- **`run.py`**: Arquivo principal para executar a aplicação.
- **`requirements.txt`**: Lista de dependências do projeto.

## 3. Implementação

### 3.1. Instalação das Dependências

No arquivo `requirements.txt`, adicione as seguintes dependências:

```plaintext
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
```

Instale as dependências executando:

```bash
pip install -r requirements.txt
```

### 3.2. Configuração Inicial

No arquivo `config/config.py`, configure a aplicação:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_muito_segura'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3.3. Modelo de Dados

No arquivo `app/models/cliente_model.py`, defina o modelo de dados:

```python
from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nome}>'
```

### 3.4. Serviço de Cliente

No arquivo `app/services/cliente_service.py`, implemente a lógica de negócio:

```python
from app.models.cliente_model import Cliente
from app import db

class ClienteService:
    @staticmethod
    def criar_cliente(nome, email):
        cliente = Cliente(nome=nome, email=email)
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def buscar_cliente_por_id(id):
        return Cliente.query.get(id)

    @staticmethod
    def buscar_todos_clientes():
        return Cliente.query.all()

    @staticmethod
    def atualizar_cliente(id, nome=None, email=None):
        cliente = Cliente.query.get(id)
        if cliente:
            if nome:
                cliente.nome = nome
            if email:
                cliente.email = email
            db.session.commit()
        return cliente

    @staticmethod
    def deletar_cliente(id):
        cliente = Cliente.query.get(id)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()
        return cliente

    @staticmethod
    def contar_clientes():
        return Cliente.query.count()
```

### 3.5. Controlador de Cliente

No arquivo `app/controllers/cliente_controller.py`, implemente os endpoints:

```python
from flask import request, jsonify
from app.services.cliente_service import ClienteService
from app.views.cliente_view import formatar_cliente

def criar_cliente():
    dados = request.json
    cliente = ClienteService.criar_cliente(dados['nome'], dados['email'])
    return jsonify(formatar_cliente(cliente)), 201

def buscar_cliente_por_id(id):
    cliente = ClienteService.buscar_cliente_por_id(id)
    if cliente:
        return jsonify(formatar_cliente(cliente))
    return jsonify({"mensagem": "Cliente não encontrado"}), 404

def buscar_todos_clientes():
    clientes = ClienteService.buscar_todos_clientes()
    return jsonify([formatar_cliente(cliente) for cliente in clientes])

def atualizar_cliente(id):
    dados = request.json
    cliente = ClienteService.atualizar_cliente(id, dados.get('nome'), dados.get('email'))
    if cliente:
        return jsonify(formatar_cliente(cliente))
    return jsonify({"mensagem": "Cliente não encontrado"}), 404

def deletar_cliente(id):
    cliente = ClienteService.deletar_cliente(id)
    if cliente:
        return jsonify({"mensagem": "Cliente deletado com sucesso"})
    return jsonify({"mensagem": "Cliente não encontrado"}), 404

def contar_clientes():
    total = ClienteService.contar_clientes()
    return jsonify({"total_clientes": total})
```

### 3.6. Visualização de Cliente

No arquivo `app/views/cliente_view.py`, formate os dados para a resposta:

```python
def formatar_cliente(cliente):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email
    }
```

### 3.7. Configuração do Flask

No arquivo `app/__init__.py`, configure o Flask e o banco de dados:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from app.controllers.cliente_controller import (
            criar_cliente, buscar_cliente_por_id, buscar_todos_clientes,
            atualizar_cliente, deletar_cliente, contar_clientes
        )

        app.route('/clientes', methods=['POST'])(criar_cliente)
        app.route('/clientes/<int:id>', methods=['GET'])(buscar_cliente_por_id)
        app.route('/clientes', methods=['GET'])(buscar_todos_clientes)
        app.route('/clientes/<int:id>', methods=['PUT'])(atualizar_cliente)
        app.route('/clientes/<int:id>', methods=['DELETE'])(deletar_cliente)
        app.route('/clientes/contar', methods=['GET'])(contar_clientes)

        db.create_all()

    return app
```

### 3.8. Executando a Aplicação

No arquivo `run.py`, execute a aplicação:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

## 4. Testando a API

Você pode testar a API usando ferramentas como **Postman** ou **curl**. Aqui estão alguns exemplos de requisições:

- **Criar Cliente**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"nome": "João", "email": "joao@example.com"}' http://localhost:5000/clientes
  ```

- **Buscar Cliente por ID**:
  ```bash
  curl -X GET http://localhost:5000/clientes/1
  ```

- **Buscar Todos os Clientes**:
  ```bash
  curl -X GET http://localhost:5000/clientes
  ```

- **Atualizar Cliente**:
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"nome": "João Silva"}' http://localhost:5000/clientes/1
  ```

- **Deletar Cliente**:
  ```bash
  curl -X DELETE http://localhost:5000/clientes/1
  ```

- **Contar Clientes**:
  ```bash
  curl -X GET http://localhost:5000/clientes/contar
  ```

## 5. Diagrama de Arquitetura

Você pode usar o [draw.io](https://draw.io) para criar um diagrama de arquitetura que mostre a interação entre os componentes (Model, View, Controller, Service) e o fluxo de dados.

---

**Bom trabalho!** 🚀
```
### Como Usar
1. Clone o repositório.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Execute o projeto com `python run.py`.
4. Teste os endpoints usando **Postman** ou **curl**.

Se precisar de mais ajuda, sinta-se à vontade para entrar em contato! 😊
```
