# Requisitos do Sistema - Biblioteca Comunitária

## 1. Introdução
O sistema de gerenciamento de bibliotecas comunitárias tem como objetivo facilitar o cadastro de livros, o controle de empréstimos, o registro de usuários e a divulgação de eventos culturais.  
A solução é voltada para uso em bibliotecas comunitárias localizadas em bairros de Fortaleza, como Mucuripe, Serviluz e Cais do Porto, buscando resolver a ineficiência na gestão de recursos e promover a inclusão digital (ODS 11).

---

## 2. Público-Alvo e Stakeholders
- **Bibliotecários/Administradores:** Responsáveis pelo cadastro de livros, controle de empréstimos e gestão de eventos. Necessitam de uma interface administrativa para gerir o acervo.
- **Usuários/Leitores:** Pessoas da comunidade que realizarão empréstimos de livros e participação em eventos. Inclui estudantes, moradores locais e idosos.
- **Gestores da Biblioteca:** Responsáveis por acompanhar o uso do espaço e o impacto das ações culturais.

---

## 3. Matriz de Requisitos Funcionais (RF)

Abaixo apresentamos os requisitos planejados na Etapa 1 e o status de sua implementação na Etapa 2 (N708).

### 3.1 Cadastro e Gestão
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF01** | Permitir o cadastro de livros com título, autor, categoria, etc. | ✅ **Implementado** | CRUD completo via perfil Admin. |
| **RF02** | Permitir o cadastro de usuários com dados de contato. | ✅ **Implementado** | Adicionada validação de Termos LGPD (Feedback jurídico). |
| **RF03** | Registrar empréstimos e devoluções. | 🔄 **Adaptado** | Simplificado para **Status de Disponibilidade** (Ver/Vermelho) para agilizar a consulta visual. |
| **RF04** | Emitir alertas de atraso de devolução. | ❌ **Despriorizado** | Recurso removido do MVP para focar na estabilidade do cadastro e usabilidade móvel. |
| **RF05** | Cadastrar e divulgar eventos culturais. | ✅ **Implementado** | Inclui indicadores de acessibilidade e local. |

### 3.2 Consultas e Relatórios
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF06** | Permitir a busca de livros por título, autor ou categoria. | ✅ **Implementado** | Busca textual em tempo real implementada. |
| **RF07** | Exibir histórico de empréstimos por usuário. | ❌ **Despriorizado** | Foco mantido na visualização do acervo atual disponível. |
| **RF08** | Gerar relatórios básicos de livros. | 🔄 **Adaptado** | A própria listagem filtrável serve como relatório de acervo em tempo real. |

### 3.3 Acesso e Perfis
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF09** | Possuir perfis de **Administrador** e **Usuário**. | ✅ **Implementado** | Controle de acesso (ACL) via sessão Flask. |
| **RF10** | O administrador tem acesso total. | ✅ **Implementado** | Botões de edição visíveis apenas para Admin. |
| **RF11** | O usuário consulta livros e eventos. | ✅ **Implementado** | Interface de leitura otimizada para mobile. |

---

## 4. Requisitos Não-Funcionais (Atualizado N708)

Devido a decisões arquiteturais visando agilidade, segurança e conformidade com o ambiente de execução, os requisitos técnicos foram atualizados:

### 4.1 Plataforma e Tecnologias
- **RNF01:** O sistema foi migrado de *Node.js/React* para **Python 3 + Flask**.
    * *Justificativa:* Maior robustez no tratamento de dados server-side e facilidade de manutenção futura pela comunidade.
- **RNF02:** O banco de dados foi migrado de *PostgreSQL* para **SQLite**.
    * *Justificativa:* Portabilidade total (arquivo único), eliminando a necessidade de servidores de banco dedicados nas bibliotecas comunitárias.
- **RNF03:** A arquitetura mudou de *API REST Pura* para **MVT (Model-View-Template)**.
    * *Justificativa:* Renderização no servidor (Jinja2) garante carregamento mais rápido em dispositivos móveis antigos comuns na comunidade.

### 4.2 Usabilidade
- **RNF04:** A interface deve ser responsiva (Web Mobile), adaptando-se a telas de smartphones (Bootstrap 5).
- **RNF05:** O sistema deve adotar padrões visuais de alto contraste e clareza (Feedback de cores para status).

### 4.3 Segurança e Desempenho
- **RNF06:** Autenticação obrigatória para áreas administrativas (Sessões seguras).
- **RNF07:** Senhas armazenadas não podem ser texto plano (Implementado hash ou mascaramento básico para MVP).
- **RNF09:** O tempo de resposta deve ser inferior a 2 segundos (Garantido pela leveza do Flask/SQLite).

---

## 5. Justificativa de Mudanças no Escopo

Conforme permitido nas orientações da disciplina ("Justifiquem eventuais mudanças em relação ao planejamento original"), realizamos as seguintes adaptações:

1.  **Foco na "Disponibilidade" em vez de "Multa" (RF03/RF04):** Durante a validação com o público-alvo, identificou-se que a dor principal do usuário era saber **se o livro está na estante** antes de sair de casa. O cálculo de multas complexo foi substituído por um indicador visual claro de disponibilidade, atendendo melhor a necessidade imediata da comunidade.
2.  **Simplificação da Infraestrutura:** A mudança para Python/SQLite permite que o sistema rode em qualquer computador simples da biblioteca, sem depender de configurações complexas de nuvem ou servidores SQL pesados, garantindo a sustentabilidade do projeto a longo prazo.
