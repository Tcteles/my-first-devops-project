import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Busca a chave secreta diretamente do cofre (Variável de Ambiente)
DATABASE_URL = os.environ.get('DATABASE_URL')

# Puxa o token de segurança do cofre
API_TOKEN = os.environ.get('API_TOKEN')

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
    return 'API DevOps Dinâmica - Autenticação Ativa - Conectada ao PostgreSQL com Sucesso!'

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    """Rota para listar todas as tarefas salvas no banco. Qualquer um ainda pode LER a lista"""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo FROM tarefas')
    linhas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    tarefas = [{"id": l[0], "titulo": l[1]} for l in linhas]
    return jsonify(tarefas)
    
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    # 🔒 BARREIRA DE SEGURANÇA: Verifica se quem enviou o cURL mandou o token certo
    token_recebido = request.headers.get('Authorization')
    
    if not token_recebido or token_recebido != f"Bearer {API_TOKEN}":
        return jsonify({"erro": "Acesso Negado! Token de seguranca invalido ou ausente."}), 401

    # Se o token estiver certo, ele deixa gravar no banco
    dados = request.get_json()
    titulo = dados.get('titulo')
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (titulo) VALUES (%s)', (titulo,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"status": "Tarefa salva com segurança!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
