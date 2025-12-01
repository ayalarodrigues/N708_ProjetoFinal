from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# --- CONFIGURAÇÕES INICIAIS ---
# Aqui eu pego o caminho exato da pasta onde esse arquivo tá, pra não ter erro de "File not found"
base_dir = os.path.dirname(os.path.abspath(__file__))

# Defino onde estão as pastas de HTML (templates) e CSS (static) voltando pastas (../../)
template_dir = os.path.join(base_dir, '../../frontend/web/templates')
static_dir = os.path.join(base_dir, '../../frontend/web/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'chave_super_secreta_projeto_unifor' # Chave pra criptografar a sessão do usuário

# Caminho do banco de dados SQLite
DB_PATH = os.path.join(base_dir, '../../database/biblioteca.db')

# Função auxiliar pra conectar no banco sem repetir código toda hora
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Isso ajuda a pegar as colunas pelo nome (ex: user['email'])
    return conn

# --- CRIAÇÃO DO BANCO ---
def init_db():
    with app.app_context():
        conn = get_db_connection()
        
        # Criando a tabela de usuários. O perfil define se é admin ou leitor.
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
        
        # Tabela de livros com o campo 'disponivel' (1 = sim, 0 = não)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT,
                autor TEXT,
                disponivel BOOLEAN DEFAULT 1
            );
        ''')
        
        # Tabela de eventos culturais
        conn.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data TEXT,
                local TEXT
            );
        ''')
        
        # --- DADOS DE TESTE (SEED) ---
        # Aqui eu crio um Admin automático se ele não existir, pra gente poder testar
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'admin@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('admin@email.com', 'admin123', 'Administrador Chefe', 'admin')")
            print("--- ADMIN CRIADO AUTOMATICAMENTE ---")

        # Crio também um leitor padrão
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'leitor@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('leitor@email.com', '123456', 'Leitor Comum', 'leitor')")

        # Se não tiver livros, cadastro alguns de exemplo
        cur.execute("SELECT count(*) FROM livros")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO livros (titulo, categoria, autor) VALUES ('Dom Casmurro', 'Romance', 'Machado de Assis')")
            conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES ('Semana do Livro', 'Feira cultural', '2025-10-15', 'Auditório')")
        
        conn.commit()
        conn.close()

# --- ROTAS DO SISTEMA ---

# Rota raiz: joga direto pro login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se for POST, é porque o usuário clicou em "Entrar"
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        # Verifica se existe esse usuário com essa senha no banco
        user = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()

        if user:
            # Salva os dados na sessão (cookie seguro)
            session['usuario'] = user['email']
            session['nome_usuario'] = user['nome']
            session['perfil'] = user['perfil'] # Importante pra saber se mostra botão de admin
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
            
    return render_template('login.html')

# Rota de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        termos = request.form.get('termos') # Checkbox do LGPD

        # Validação exigida pelo feedback jurídico
        if not termos:
            flash('Você precisa aceitar os termos de uso.', 'warning')
            return render_template('cadastro.html')

        try:
            conn = get_db_connection()
            # Por padrão, todo mundo que se cadastra é 'leitor'
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES (?, ?, ?, 'leitor')", (email, senha, nome))
            conn.commit()
            conn.close()
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # Se der erro de integridade, é porque o email já existe (UNIQUE no banco)
            flash('Este email já está cadastrado.', 'danger')

    return render_template('cadastro.html')

# Página Inicial (Menu)
@app.route('/home')
def home():
    # Proteção: se não tiver logado, manda pro login
    if 'usuario' not in session: return redirect(url_for('login'))
    return render_template('home.html')

# Listagem de Livros + Busca
@app.route('/livros')
def livros():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    pesquisa = request.args.get('q') # Pega o que foi digitado na busca
    conn = get_db_connection()
    
    if pesquisa:
        # Busca aprimorada: procura no Título, Autor ou Categoria (SQL com LIKE)
        termo = '%' + pesquisa + '%'
        livros = conn.execute("""
            SELECT * FROM livros 
            WHERE titulo LIKE ? OR autor LIKE ? OR categoria LIKE ?
        """, (termo, termo, termo)).fetchall()
        
        if not livros:
            flash(f'Nenhum livro encontrado para "{pesquisa}".', 'warning')
    else:
        # Se não buscou nada, traz tudo
        livros = conn.execute('SELECT * FROM livros').fetchall()
    
    conn.close()
    return render_template('livros.html', livros=livros)

# Adicionar Livro (Restrito para Admin)
@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    # Verificação de segurança: só admin passa daqui
    if session.get('perfil') != 'admin': 
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

# Listagem de Eventos
@app.route('/eventos')
def eventos():
    if 'usuario' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM eventos').fetchall()
    conn.close()
    return render_template('eventos.html', eventos=eventos)

# Adicionar Evento (Restrito para Admin)
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

# Rota de Empréstimo e Devolução
@app.route('/livros/emprestar/<int:livro_id>')
def alternar_emprestimo(livro_id):
    """
    Lógica do Empréstimo:
    - Se tá disponível -> Qualquer um pega emprestado.
    - Se tá emprestado -> Só o Admin pode devolver (segurança).
    """
    if 'usuario' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (livro_id,)).fetchone()
    
    if livro:
        if livro['disponivel']: 
            # Pegando emprestado
            novo_status = 0
            acao = "emprestado"
        else:
            # Devolvendo (Regra de negócio: Só admin confirma devolução)
            if session.get('perfil') != 'admin':
                flash('Apenas administradores podem confirmar a devolução do livro.', 'danger')
                conn.close()
                return redirect(url_for('livros'))
            
            novo_status = 1
            acao = "devolvido"

        conn.execute('UPDATE livros SET disponivel = ? WHERE id = ?', (novo_status, livro_id))
        conn.commit()
        flash(f'Livro {acao} com sucesso!', 'success')
    
    conn.close()
    return redirect(url_for('livros'))

# Logout
@app.route('/logout')
def logout():
    session.clear() # Limpa a sessão pra ninguém entrar de novo sem senha
    return redirect(url_for('login'))

# Página 404 personalizada (pra ficar mais bonito se errar o link)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- INICIALIZAÇÃO ---
# Garante que o banco existe antes de tudo (importante pro Railway)
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

init_db() 

if __name__ == '__main__':
    # Pega a porta do ambiente ou usa 5000 se eu tiver rodando no meu PC
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)