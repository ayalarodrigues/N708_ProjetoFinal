from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# --- CONFIGURAÇÕES DO PROJETO ---
# Aqui eu pego o diretório atual pra garantir que o Python ache os arquivos
# independente de onde o comando for rodado (evita erro de TemplateNotFound)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Aponto manualmente onde estão as pastas do frontend
template_dir = os.path.join(base_dir, '../../frontend/web/templates')
static_dir = os.path.join(base_dir, '../../frontend/web/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Chave secreta necessária pro Flask gerenciar a sessão (cookies) com segurança
app.secret_key = 'chave_super_secreta_projeto_unifor'

# Defini o caminho do banco aqui pra ser fácil de achar
DB_PATH = os.path.join(base_dir, '../../database/biblioteca.db')

# Função auxiliar que criei pra não ficar repetindo a conexão toda hora
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    # Isso é importante: permite acessar as colunas pelo nome (ex: livro['titulo'])
    conn.row_factory = sqlite3.Row
    return conn

# --- INICIALIZAÇÃO DO BANCO DE DADOS ---
def init_db():
    with app.app_context():
        conn = get_db_connection()
        
        # Tabela de Usuários: O campo 'perfil' define se é admin ou leitor
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                nome TEXT,
                endereco TEXT,
                perfil TEXT DEFAULT 'leitor'
            );
        ''')
        
        # Tabela de Livros: Adicionei 'emprestado_por' pra saber com quem está o livro
        conn.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT,
                autor TEXT,
                disponivel BOOLEAN DEFAULT 1,
                emprestado_por TEXT
            );
        ''')
        
        # Tabela de Eventos
        conn.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data TEXT,
                local TEXT
            );
        ''')
        
        # --- DADOS DE EXEMPLO (SEED) ---
        # Verifico se já tem admin. Se não tiver, crio um padrão pra gente conseguir testar.
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'admin@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('admin@email.com', 'admin123', 'Administrador Chefe', 'admin')")
            print("--- ADMIN PADRÃO CRIADO ---")

        # Crio um leitor de teste também
        cur.execute("SELECT count(*) FROM usuarios WHERE email = 'leitor@email.com'")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES ('leitor@email.com', '123456', 'Leitor Comum', 'leitor')")

        # Se a biblioteca estiver vazia, adiciono uns livros e eventos iniciais
        cur.execute("SELECT count(*) FROM livros")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO livros (titulo, categoria, autor) VALUES ('Dom Casmurro', 'Romance', 'Machado de Assis')")
            conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES ('Semana do Livro', 'Feira cultural', '2025-10-15', 'Auditório')")
        
        conn.commit()
        conn.close()

# --- ROTAS E LÓGICA DO SISTEMA ---

@app.route('/')
def index():
    # Se entrar na raiz, manda direto pro login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = get_db_connection()
        # Busca o usuário no banco
        user = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()

        if user:
            # Login com sucesso: Guardo as infos na sessão
            session['usuario'] = user['email']
            session['nome_usuario'] = user['nome']
            session['perfil'] = user['perfil'] # Guardo o perfil pra usar nas proteções de rota
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Pegando dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        termos = request.form.get('termos')

        # Validação importante: Se não marcar o checkbox da LGPD, não deixa cadastrar
        if not termos:
            flash('Você precisa aceitar os termos de uso.', 'warning')
            return render_template('cadastro.html')

        try:
            conn = get_db_connection()
            # Todo cadastro novo entra como 'leitor' por segurança
            conn.execute("INSERT INTO usuarios (email, senha, nome, perfil) VALUES (?, ?, ?, 'leitor')", (email, senha, nome))
            conn.commit()
            conn.close()
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # O banco avisa se o email já existe (UNIQUE constraint)
            flash('Este email já está cadastrado.', 'danger')

    return render_template('cadastro.html')

@app.route('/home')
def home():
    # Verificação de segurança: se não tiver logado, expulsa pro login
    if 'usuario' not in session: return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/livros')
def livros():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    pesquisa = request.args.get('q')
    conn = get_db_connection()
    
    if pesquisa:
        # Implementei uma busca universal: procura no título, autor OU categoria
        termo = '%' + pesquisa + '%'
        livros = conn.execute("""
            SELECT * FROM livros 
            WHERE titulo LIKE ? OR autor LIKE ? OR categoria LIKE ?
        """, (termo, termo, termo)).fetchall()
        
        if not livros:
            flash(f'Nenhum livro encontrado para "{pesquisa}".', 'warning')
    else:
        # Se não tiver busca, lista tudo
        livros = conn.execute('SELECT * FROM livros').fetchall()
    
    conn.close()
    return render_template('livros.html', livros=livros)

# Rota exclusiva para Admin cadastrar livros
@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    if 'usuario' not in session: return redirect(url_for('login'))
    
    # Bloqueio de segurança: Se não for admin, não entra
    if session.get('perfil') != 'admin': 
        flash('Acesso negado. Apenas administradores podem cadastrar livros.', 'danger')
        return redirect(url_for('livros'))

    if request.method == 'POST':
        # Salva o livro no banco
        conn = get_db_connection()
        conn.execute("INSERT INTO livros (titulo, autor, categoria) VALUES (?, ?, ?)", 
                     (request.form['titulo'], request.form['autor'], request.form['categoria']))
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

# Rota exclusiva para Admin criar eventos
@app.route('/eventos/adicionar', methods=['GET', 'POST'])
def adicionar_evento():
    if 'usuario' not in session: return redirect(url_for('login'))
    if session.get('perfil') != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('eventos'))

    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("INSERT INTO eventos (titulo, descricao, data, local) VALUES (?, ?, ?, ?)", 
                     (request.form['titulo'], request.form['descricao'], request.form['data'], request.form['local']))
        conn.commit()
        conn.close()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('eventos'))

    return render_template('novo_evento.html')

# Lógica de Empréstimo e Devolução
@app.route('/livros/emprestar/<int:livro_id>')
def alternar_emprestimo(livro_id):
    if 'usuario' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (livro_id,)).fetchone()
    
    if livro:
        if livro['disponivel']: 
            # CENÁRIO 1: PEGAR EMPRESTADO
            # Qualquer usuário pode pegar. Eu gravo o nome dele pra saber com quem está.
            conn.execute('UPDATE livros SET disponivel = 0, emprestado_por = ? WHERE id = ?', 
                         (session['nome_usuario'], livro_id))
            acao = "emprestado"
        else:
            # CENÁRIO 2: DEVOLVER
            # Só o Admin pode dar baixa na devolução pra garantir que o livro voltou mesmo
            if session.get('perfil') != 'admin':
                flash('Apenas administradores podem confirmar a devolução.', 'danger')
                conn.close()
                return redirect(url_for('livros'))
            
            # Limpo o campo 'emprestado_por' e deixo disponível de novo
            conn.execute('UPDATE livros SET disponivel = 1, emprestado_por = NULL WHERE id = ?', (livro_id,))
            acao = "devolvido"

        conn.commit()
        flash(f'Livro {acao} com sucesso!', 'success')
    
    conn.close()
    return redirect(url_for('livros'))

@app.route('/logout')
def logout():
    session.clear() # Limpa a sessão e desloga
    return redirect(url_for('login'))

# Página de erro personalizada pra melhorar a UX
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- INICIALIZAÇÃO ---
# Garante que a pasta e o banco existam antes de rodar (essencial pro Railway)
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

init_db() 

if __name__ == '__main__':
    # Pega a porta do ambiente (Railway) ou usa 5000 se for local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)