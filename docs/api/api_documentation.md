# Documentação da Interface de Controle (Rotas)

Este documento detalha os endpoints do controlador principal (`app.py`). O sistema utiliza a arquitetura **MVT (Model-View-Template)**, onde as rotas processam a lógica de negócio e retornam templates HTML renderizados via Jinja2.

---

## 1. Mapeamento de Rotas

### Autenticação e Usuários

| Método | Rota        | Descrição                                          | Acesso  |
| ------ | ----------- | -------------------------------------------------- | ------- |
| `GET`  | `/login`    | Exibe o formulário de autenticação.                | Público |
| `POST` | `/login`    | Processa as credenciais e inicia a sessão segura.  | Público |
| `GET`  | `/cadastro` | Exibe o formulário de registro de novos leitores.  | Público |
| `POST` | `/cadastro` | Cria novo usuário no banco (Valida aceite LGPD).   | Público |
| `GET`  | `/logout`   | Encerra a sessão atual e redireciona para o login. | Logado  |

### Gestão de Acervo (Livros)

| Método | Rota                     | Descrição                                                                                                  | Acesso    |
| ------ | ------------------------ | ---------------------------------------------------------------------------------------------------------- | --------- |
| `GET`  | `/livros`                | Lista todo o acervo com indicadores visuais de status.                                                     | Logado    |
| `GET`  | `/livros?q={termo}`      | **Busca Universal:** Filtra por Título, Autor ou Categoria.                                                | Logado    |
| `GET`  | `/livros/emprestar/{id}` | **Alternar Status (Toggle):**<br>1. Se disponível: Registra empréstimo para o usuário logado.<br>2. Se emprestado: Realiza devolução (Ação restrita a **Administradores** para conferência física). | Logado |
| `GET`  | `/livros/adicionar`      | Exibe formulário de cadastro de livro.                                                                     | **Admin** |
| `POST` | `/livros/adicionar`      | Salva o novo livro no banco de dados.                                                                      | **Admin** |

### Eventos Culturais

| Método | Rota                 | Descrição                                           | Acesso    |
| ------ | -------------------- | --------------------------------------------------- | --------- |
| `GET`  | `/eventos`           | Lista a agenda cultural com info de acessibilidade. | Logado    |
| `GET`  | `/eventos/adicionar` | Exibe formulário de criação de evento.              | **Admin** |
| `POST` | `/eventos/adicionar` | Salva o novo evento na agenda.                      | **Admin** |

---

## 2. Estrutura de Dados (Formulários)

Como o sistema utiliza renderização no servidor, os dados são trafegados via `application/x-www-form-urlencoded` (Form Data).

### Cadastro de Usuário (`POST /cadastro`)

```python
{
    "nome": "String (Obrigatório)",
    "email": "String (Obrigatório, Único)",
    "senha": "String (Obrigatório)",
    "endereco": "String (Obrigatório)",
    "termos": "Checkbox (Deve estar marcado 'on' para validar LGPD)"
}
```

### Cadastro de Livro (`POST /livros/adicionar`)

```python
{
    "titulo": "String (Obrigatório)",
    "autor": "String (Obrigatório)",
    "categoria": "String (Select: Romance, Técnico, Infantil, etc)"
}
```

### Cadastro de Evento (`POST /eventos/adicionar`)

```python
{
    "titulo": "String (Obrigatório)",
    "descricao": "String (Texto longo)",
    "data": "Date (YYYY-MM-DD)",
    "local": "String (Ex: Auditório, Sala 3)"
}
```

### Filtros de Busca (`GET /livros`)

```python
{
    "q": "String (Busca parcial em Título OR Autor OR Categoria)"
}
```

---

## 3. Códigos de Retorno HTTP

Embora não seja uma API JSON, o sistema respeita os códigos de status HTTP para renderização:

* **200 OK:** Página carregada com sucesso.
* **302 Found:** Redirecionamento (ex: após login ou cadastro com sucesso).
* **404 Not Found:** Recurso não encontrado (Página personalizada implementada).
* **500 Internal Server Error:** Erro crítico no servidor.
