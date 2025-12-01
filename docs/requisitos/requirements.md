# Requisitos do Sistema - Biblioteca Comunitária

## 1. Introdução e Contextualização
O sistema destina-se à gestão de **bibliotecas comunitárias**: espaços culturais autônomos geridos pela sociedade civil em bairros periféricos de Fortaleza (como Mucuripe, Serviluz e Cais do Porto). Diferente de grandes bibliotecas públicas estatais, estes espaços operam com recursos limitados e mão de obra muitas vezes voluntária, carecendo de ferramentas digitais acessíveis para profissionalizar o controle do acervo e a divulgação de suas ações culturais.

O projeto foi concebido para atender diretamente ao **ODS 11 (Cidades e Comunidades Sustentáveis)** da Agenda 2030 da ONU. Ao digitalizar o acervo e facilitar o acesso à informação, a ferramenta contribui para a **meta 11.4 (Fortalecer esforços para proteger e salvaguardar o patrimônio cultural)** e promove a inclusão digital em territórios vulneráveis, tornando a cidade mais acessível e integrada.

---

## 2. Público-Alvo e Stakeholders
- **Bibliotecários/Administradores:** Geralmente voluntários ou líderes comunitários responsáveis pela organização do espaço. Necessitam de uma interface administrativa simples para gerir o acervo sem burocracia excessiva.
- **Usuários/Leitores:** Moradores da comunidade (crianças, jovens e idosos) que utilizam o espaço não apenas para empréstimo de livros, mas como ponto de encontro e aprendizado.
- **Gestores da Biblioteca:** Responsáveis pela sustentabilidade do projeto, que utilizam os dados de acervo para buscar editais e apoios.

---

## 3. Matriz de Requisitos Funcionais (RF)

Abaixo apresentamos os requisitos planejados na Etapa 1 e o status de sua implementação na Etapa 2 (N708).

### 3.1 Cadastro e Gestão
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF01** | Permitir o cadastro de livros com título, autor, categoria, etc. | ✅ **Implementado** | CRUD completo via perfil Admin. |
| **RF02** | Permitir o cadastro de usuários com dados de contato. | ✅ **Implementado** | Adicionada validação de Termos LGPD (Feedback jurídico). |
| **RF03** | Registrar empréstimos e devoluções. | 🔄 **Adaptado** | Simplificado para **Status de Disponibilidade** (Verde/Vermelho) para agilizar a consulta visual imediata. |
| **RF04** | Emitir alertas de atraso de devolução. | ❌ **Despriorizado** | Recurso removido do MVP para focar na estabilidade do cadastro e usabilidade móvel. |
| **RF05** | Cadastrar e divulgar eventos culturais. | ✅ **Implementado** | Inclui indicadores de acessibilidade e local. |

### 3.2 Consultas e Relatórios
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF06** | Permitir a busca de livros por título, autor ou categoria. | ✅ **Implementado** | Busca textual em tempo real implementada. |
| **RF07** | Exibir histórico de empréstimos por usuário. | ❌ **Despriorizado** | Foco mantido na visualização do acervo atual disponível para a comunidade. |
| **RF08** | Gerar relatórios básicos de livros. | 🔄 **Adaptado** | A própria listagem filtrável serve como relatório de acervo em tempo real. |

### 3.3 Acesso e Perfis
| ID | Descrição Original | Status na Entrega | Observação |
|:---:|---|:---:|---|
| **RF09** | Possuir perfis de **Administrador** e **Usuário**. | ✅ **Implementado** | Controle de acesso (ACL) via sessão Flask. |
| **RF10** | O administrador tem acesso total. | ✅ **Implementado** | Botões de edição visíveis apenas para Admin. |
| **RF11** | O usuário consulta livros e eventos. | ✅ **Implementado** | Interface de leitura otimizada para mobile. |

---

## 4. Requisitos Não-Funcionais (Atualizado N708)

Devido a decisões arquiteturais visando agilidade, segurança e conformidade com o ambiente de execução (computadores modestos), os requisitos técnicos foram atualizados:

### 4.1 Plataforma e Tecnologias
- **RNF01:** O sistema foi migrado de *Node.js/React* para **Python 3 + Flask**.
    * *Justificativa:* Maior robustez no tratamento de dados server-side e facilidade de manutenção futura pela comunidade.
- **RNF02:** O banco de dados foi migrado de *PostgreSQL* para **SQLite**.
    * *Justificativa:* Portabilidade total (arquivo único), eliminando a necessidade de servidores de banco dedicados e custos de nuvem.
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

Conforme permitido nas orientações da disciplina ("Justifiquem eventuais mudanças em relação ao planejamento original"), realizamos as seguintes adaptações para garantir a entrega de valor real:

1.  **Foco na "Disponibilidade" em vez de "Multa" (RF03/RF04):** Durante a validação com o público-alvo, identificou-se que a dor principal do morador era saber **se o livro está na estante** antes de se deslocar até a biblioteca. O cálculo de multas complexo foi substituído por um indicador visual claro de disponibilidade, atendendo melhor a necessidade imediata da comunidade e incentivando o uso do espaço (ODS 11).
2.  **Simplificação da Infraestrutura:** A mudança para Python/SQLite permite que o sistema rode em qualquer computador simples da biblioteca, garantindo a sustentabilidade do projeto a longo prazo sem custos de infraestrutura complexa.
