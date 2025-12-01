# Modelo de Dados - Biblioteca Comunitária

## 1. Visão Geral
O banco de dados foi implementado utilizando **SQLite 3**. Esta escolha garante que o sistema seja **autocontido** (o banco é um arquivo `.db`), facilitando backups (basta copiar o arquivo) e a implantação em computadores modestos das bibliotecas comunitárias, sem a necessidade de configurar servidores de banco de dados complexos.

---

## 2. Diagrama Entidade-Relacionamento (DER)

O diagrama abaixo representa a estrutura lógica das entidades principais do sistema e seus relacionamentos. Na implementação física (SQLite), algumas restrições são gerenciadas pela camada de aplicação (Python/Flask) para garantir a integridade.


---

## 3. Esquema Físico (DDL Implementado)

Abaixo, o esquema exato utilizado pelo script de inicialização (`app.py`) para criar o banco de dados:

```sql
-- ==================================================
-- Tabela: Usuários
-- Armazena leitores e administradores (diferenciados pelo campo 'perfil')
-- ==================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL, -- Senha armazenada (hash recomendado para produção)
    nome TEXT,
    endereco TEXT,
    perfil TEXT DEFAULT 'leitor' -- Controle de ACL: 'admin' ou 'leitor'
);

-- ==================================================
-- Tabela: Livros (Acervo)
-- Controla o catálogo e a disponibilidade imediata
-- ==================================================
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    categoria TEXT,
    autor TEXT,
    disponivel BOOLEAN DEFAULT 1, -- 1 = Disponível na estante, 0 = Emprestado
    emprestado_por TEXT -- Armazena o nome do usuário responsável pelo empréstimo
);

-- ==================================================
-- Tabela: Eventos (Agenda Cultural)
-- Divulgação de ações da biblioteca para a comunidade
-- ==================================================
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data TEXT,
    local TEXT
);
