from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__, template_folder='../../frontend/web/templates', static_folder='../../frontend/web/static')
app.secret_key = 'chave_super_secreta_projeto_unifor'

# Configuração do Banco de Dados
DB_PATH = os.path.join(os.path.dirname(__file__), '../../database/biblioteca.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        # Criação das tabelas baseadas no seu Diagrama ER
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT,
                endereco TEXT
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT,
                autor TEXT,
                disponivel BOOLEAN DEFAULT 1
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data TEXT,
                local TEXT
            );
        ''')
        
        # Inserir dados falsos para teste (Popula o banco)
        # Verifica se já tem livros
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM livros")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO livros (titulo, categoria, autor) VALUES ('Dom Casmurro', 'Romance', 'Machado de Assis')")
            conn.execute("INSERT INTO livros (titulo, categoria, autor) VALUES ('E o Vento Levou', 'Romance', 'Margaret Mitchell')")
            conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES ('Semana do Livro', 'Palestra e feira', '15/10/2025', 'Auditório')")
        
        conn.commit()
        conn.close()

# Rotas (Endpoints)
@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login "fictício" que aceita qualquer coisa para teste rápido, 
        session['usuario'] = request.form['email']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Lógica de salvar no banco
        nome = request.form['nome']
        email = request.form['email']
        # Aqui entra o Checkbox do Feedback (Arthur Soares)
        termos = request.form.get('termos')
        if not termos:
             return "Erro: Aceite os termos (LGPD)"
        
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/home')
def home():
    if 'usuario' not in session: return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/livros')
def livros():
    if 'usuario' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()
    return render_template('livros.html', livros=livros)

@app.route('/eventos')
def eventos():
    if 'usuario' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM eventos').fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)