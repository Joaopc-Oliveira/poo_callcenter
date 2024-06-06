from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('../database/hamburgueria.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def modify_db(query, args=()):
    conn = sqlite3.connect('../database/hamburgueria.db')
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

@app.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = query_db('SELECT * FROM clientes')
    return jsonify([dict(cliente) for cliente in clientes])

@app.route('/hamburgueres', methods=['GET'])
def get_hamburgueres():
    hamburgueres = query_db('SELECT * FROM hamburgueres')
    return jsonify([dict(hamburguer) for hamburguer in hamburgueres])

@app.route('/hamburgueres/search', methods=['GET'])
def search_hamburgueres():
    query = request.args.get('query', '')
    hamburgueres = query_db('SELECT * FROM hamburgueres WHERE nome_hamburguer LIKE ?', [f'%{query}%'])
    return jsonify([dict(hamburguer) for hamburguer in hamburgueres])

@app.route('/pedidos', methods=['POST'])
def add_pedido():
    data = request.json
    now = datetime.now()
    client = query_db('SELECT * FROM clientes WHERE id_cliente = ?', [data['id_cliente']], one=True)
    if not client:
        modify_db('INSERT INTO clientes (id_cliente, nome, morada, telefone) VALUES (?, ?, ?, ?)',
                  (data['id_cliente'], data['nome_cliente'], data['morada_cliente'], data['telefone_cliente']))
    modify_db('''
        INSERT INTO pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, data_hora, valor_total)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['id_cliente'], data['nome_hamburguer'], data['quantidade'], data['tamanho'], now, data['valor_total']))
    return jsonify({'message': 'Pedido adicionado com sucesso!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == 'admin123':
        return jsonify({'message': 'Login successful!'})
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/clientes/search', methods=['GET'])
def search_clientes():
    nome = request.args.get('nome', '')
    telefone = request.args.get('telefone', '')
    query = 'SELECT * FROM clientes WHERE 1=1'
    args = []
    if nome:
        query += ' AND nome LIKE ?'
        args.append(f'%{nome}%')
    if telefone:
        query += ' AND telefone LIKE ?'
        args.append(f'%{telefone}%')
    clientes = query_db(query, args)
    return jsonify([dict(cliente) for cliente in clientes])

@app.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    data = request.args.get('data')
    if not data:
        return jsonify({'message': 'Data não fornecida'}), 400
    query = '''
        SELECT id_cliente, nome_hamburguer, quantidade, tamanho, valor_total
        FROM pedidos
        WHERE date(data_hora) = ?
    '''
    estatisticas = query_db(query, [data])
    return jsonify([dict(estatistica) for estatistica in estatisticas])

if __name__ == '__main__':
    app.run(debug=True)
