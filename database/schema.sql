-- Esquema do Banco de Dados SQLite (Biblioteca Comunitária)

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nome TEXT,
    endereco TEXT,
    perfil TEXT DEFAULT 'leitor' -- 'admin' ou 'leitor'
);

CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    categoria TEXT,
    autor TEXT,
    disponivel BOOLEAN DEFAULT 1, -- 1 = Disponível, 0 = Indisponível
    emprestado_por TEXT -- Nome do usuário que pegou emprestado (Rastreabilidade)
);

CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data TEXT,
    local TEXT
);
