# Especificação de Rotas e Interface (Flask)

O sistema utiliza arquitetura RESTful nas rotas, porém retorna interfaces renderizadas (HTML) em vez de JSON puro, facilitando a indexação e a compatibilidade com navegadores antigos.

## 1. Mapeamento de Rotas

### Autenticação e Usuários
| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `GET` | `/login` | Exibe formulário de login | Público |
| `POST` | `/login` | Processa credenciais e inicia sessão | Público |
| `GET` | `/cadastro` | Exibe formulário de registro | Público |
| `POST` | `/cadastro` | Cria novo usuário (Valida LGPD) | Público |
| `GET` | `/logout` | Encerra sessão | Logado |

### Gestão de Acervo
| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `GET` | `/livros` | Lista acervo e status de disponibilidade | Logado |
| `GET` | `/livros?q=termo` | Busca livros por título | Logado |
| `GET` | `/livros/adicionar`| Exibe form de novo livro | **Admin** |
| `POST` | `/livros/adicionar`| Salva novo livro no banco | **Admin** |

### Eventos Culturais
| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| `GET` | `/eventos` | Lista agenda cultural | Logado |
| `GET` | `/eventos/adicionar`| Exibe form de novo evento | **Admin** |
| `POST` | `/eventos/adicionar`| Salva novo evento | **Admin** |

---

## 2. Estrutura de Dados (Formulários)

Exemplo de Payload para Cadastro de Livro (`POST /livros/adicionar`):
```python
{
    "titulo": "String (Obrigatório)",
    "autor": "String (Obrigatório)",
    "categoria": "String (Select: Romance, Técnico, etc)"
}
