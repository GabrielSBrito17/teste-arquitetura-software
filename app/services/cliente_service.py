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