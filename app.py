from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

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

def create_user_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin'))
    conn.commit()
    conn.close()
    print("Tabela de usuários criada com sucesso")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('cadastro'))
        else:
            error = "Credenciais inválidas. Tente novamente."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/listar_clientes')
def listar_clientes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    create_user_table()
    app.run(debug=True)
