# Relatório de Validação com Público-Alvo

## 1. Perfil do Validador e Contexto

A validação foi conduzida com um representante estratégico da comunidade, selecionado para garantir que o sistema atenda tanto às necessidades locais quanto aos requisitos legais de proteção de dados.

* **Nome:** Arthur Nogueira Soares
* **Perfil:** Morador do bairro Mucuripe e Advogado.
* **Justificativa:** Sua inserção na comunidade valida a usabilidade para o público final, enquanto sua formação jurídica oferece uma auditoria sobre a conformidade do sistema (LGPD), essencial para a segurança da instituição.

---

## 2. Metodologia

* **Data:** 22/11/2025
* **Formato:** Videoconferência via Google Meet (Devido à disponibilidade do entrevistado).
* **Técnica:** Entrevista com Demonstração Guiada (*Walkthrough*). O entrevistador compartilhou a tela e navegou pelo sistema em tempo real, solicitando ao usuário que descrevesse suas impressões e dúvidas a cada funcionalidade apresentada.
* **Evidências:** As capturas de tela da sessão e o Termo de Uso de Imagem assinado encontram-se na pasta `validation/evidence/`.

---

## 3. Feedbacks Coletados e Análise

Durante a sessão, foram identificados três pontos críticos que exigiram intervenção na equipe de desenvolvimento:

### Feedback 1: Transparência e LGPD (Crítico)
* **Contexto:** Tela de Cadastro de Usuário.
* **Comentário do Usuário:** *"Eu vi que vocês pedem Endereço. Como advogado, sinto falta de um 'li e concordo'. Eu preciso saber como a biblioteca vai usar meu endereço. Sem isso, a biblioteca corre risco jurídico."*
* **Análise:** O sistema original coletava dados sensíveis sem consentimento explícito, violando princípios da LGPD.

### Feedback 2: Clareza no Status do Livro (Médio)
* **Contexto:** Listagem de Livros.
* **Comentário do Usuário:** *"A lista está bonita, mas olhando para 'Dom Casmurro', eu não sei se ele está na estante agora ou se o vizinho pegou. Eu teria que ir até lá só para descobrir?"*
* **Análise:** A interface não comunicava a disponibilidade imediata, frustrando o objetivo de evitar deslocamentos desnecessários (ODS 11).

### Feedback 3: Acessibilidade nos Eventos (Baixo/Melhoria)
* **Contexto:** Detalhes do Evento.
* **Comentário do Usuário:** *"Moro aqui no Mucuripe e é difícil saber onde ficam as salas. Seria ótimo saber se tem acessibilidade, pois gostaria de levar minha mãe que é idosa."*
* **Análise:** Falta de informações inclusivas limitava o público-alvo dos eventos.

---

## 4. Ajustes Implementados (Correções)

Com base nos feedbacks, as seguintes alterações foram realizadas no código (Python/Flask):

| Feedback | Solução Implementada | Alteração Técnica |
|---|---|---|
| **1. LGPD** | **Checkbox Obrigatório:** Inclusão de campo "Li e concordo com os termos" no cadastro. | Adicionado campo `termos` no formulário HTML e validação condicional no backend (`app.py`) que impede o registro sem o aceite. |
| **2. Status** | **Indicador Visual:** Etiquetas coloridas nos cards de livros. | Lógica no template (`livros.html`) que renderiza `<span class="badge bg-success">Disponível</span>` ou `<span class="badge bg-danger">Emprestado</span>` baseado no banco de dados. |
| **3. Inclusão** | **Info de Acessibilidade:** Novo campo nos eventos. | Adicionado atributo "Local Acessível" na modelagem de eventos e exibição destacada no card do evento (`eventos.html`). |

---

## 5. Conclusão

A validação externa foi fundamental para amadurecer o projeto. O olhar jurídico do usuário Arthur impediu que o sistema fosse lançado com vulnerabilidades legais (LGPD), enquanto sua visão de morador direcionou o foco para a "disponibilidade real" dos livros.

O sistema final, ajustado pós-validação, é significativamente mais **seguro**, **transparente** e **inclusivo** do que a versão planejada inicialmente.
