from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# Configuração de caminhos
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '../../frontend/web/templates')
static_dir = os.path.join(base_dir, '../../frontend/web/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'chave_super_secreta_projeto_unifor'

DB_PATH = os.path.join(base_dir, '../../database/biblioteca.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        
        # Tabela Usuários (com campo perfil)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                nome TEXT,
                endereco TEXT,
                perfil TEXT DEFAULT 'leitor' -- 'admin' ou 'leitor'
            );
        ''')
        
        # Tabelas de Livros e Eventos
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
        
        # --- DADOS INICIAIS (SEED) ---
        # Cria um ADMIN se não existir
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'admin@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('admin@email.com', 'admin123', 'Administrador Chefe', 'admin')")
            print("--- USUÁRIO ADMIN CRIADO: admin@email.com / senha: admin123 ---")

        # Cria um LEITOR padrão
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'leitor@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('leitor@email.com', '123456', 'Leitor Comum', 'leitor')")

        # Dados de exemplo para livros e eventos
        cur.execute("SELECT count(*) FROM livros")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO livros (titulo, categoria, autor) VALUES ('Dom Casmurro', 'Romance', 'Machado de Assis')")
            conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES ('Semana do Livro', 'Feira cultural', '2025-10-15', 'Auditório')")
        
        conn.commit()
        conn.close()

# --- ROTAS ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()

        if user:
            session['usuario'] = user['email']
            session['nome_usuario'] = user['nome']
            session['perfil'] = user['perfil'] # Guarda se é admin ou leitor
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        termos = request.form.get('termos')

        if not termos:
            flash('Você precisa aceitar os termos de uso.', 'warning')
            return render_template('cadastro.html')

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES (?, ?, ?, 'leitor')", (email, senha, nome))
            conn.commit()
            conn.close()
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Este email já está cadastrado.', 'danger')

    return render_template('cadastro.html')

@app.route('/home')
def home():
    if 'usuario' not in session: return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/livros')
def livros():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    pesquisa = request.args.get('q')
    conn = get_db_connection()
    
    if pesquisa:
        livros = conn.execute("SELECT * FROM livros WHERE titulo LIKE ?", ('%' + pesquisa + '%',)).fetchall()
        if not livros:
            flash(f'Nenhum livro encontrado para "{pesquisa}".', 'warning')
    else:
        livros = conn.execute('SELECT * FROM livros').fetchall()
    
    conn.close()
    return render_template('livros.html', livros=livros)

# ROTA NOVA: Adicionar Livro (Só Admin)
@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    if 'usuario' not in session: return redirect(url_for('login'))
    if session.get('perfil') != 'admin': # Segurança no Backend
        flash('Acesso negado. Apenas administradores podem cadastrar livros.', 'danger')
        return redirect(url_for('livros'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']
        
        conn = get_db_connection()
        conn.execute("INSERT INTO livros (titulo, autor, categoria) VALUES (?, ?, ?)", (titulo, autor, categoria))
        conn.commit()
        conn.close()
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('livros'))

    return render_template('novo_livro.html')

@app.route('/eventos')
def eventos():
    if 'usuario' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM eventos').fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

# ROTA NOVA: Adicionar Evento (Só Admin)
@app.route('/eventos/adicionar', methods=['GET', 'POST'])
def adicionar_evento():
    if 'usuario' not in session: return redirect(url_for('login'))
    if session.get('perfil') != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('eventos'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        local = request.form['local']
        
        conn = get_db_connection()
        conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES (?, ?, ?, ?)", 
                     (titulo, descricao, data, local))
        conn.commit()
        conn.close()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('eventos'))

    return render_template('novo_evento.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Garante que a pasta do banco existe
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    init_db()

    # Pega a porta do ambiente (Railway) ou usa 5000 se for local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)