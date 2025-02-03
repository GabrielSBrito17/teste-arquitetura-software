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