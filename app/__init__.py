from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

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