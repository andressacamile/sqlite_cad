from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = os.path.join(os.path.dirname(__file__), 'clientes.db')

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabela criada com sucesso")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/clientes')
def listar_clientes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    print("Clientes Cadastrados:", clientes)
    for cliente in clientes:
        print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, Email: {cliente['email']}, Telefone: {cliente['telefone']}")
    return render_template('listar_clientes.html', clientes=clientes)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
            conn.commit()
            print(f"Cliente cadastrado - Nome: {nome}, Email: {email}, Telefone: {telefone}")
        except Exception as e:
            conn.rollback()
            print(f"Erro durante o cadastro: {e}")
        finally:
            conn.close()
    return redirect(url_for('listar_clientes'))

if __name__ == '__main__':
    app.run(debug=True)
