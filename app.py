import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Busca a chave secreta diretamente do cofre (Variável de Ambiente)
DATABASE_URL = os.environ.get('DATABASE_URL')

def init_db():
    """Cria a tabela de tarefas no banco de dados se ela não existir"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Inicializa o banco de dados seguro
try:
    init_db()
except Exception as e:
    print(f"Erro ao conectar no banco de dados: {e}")

@app.route('/')
def home():
    return 'API DevOps Dinâmica - Conectada ao PostgreSQL com Sucesso!'

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    """Rota para listar todas as tarefas salvas no banco"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo FROM tarefas')
    linhas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    tarefas = [{"id": l[0], "titulo": l[1]} for l in linhas]
    return jsonify(tarefas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
