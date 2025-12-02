# Relatório de Validação e Homologação com Público-Alvo

## 1. Perfil do Validador e Contexto

A validação foi conduzida de forma iterativa com um representante estratégico da comunidade, selecionado para garantir a aderência do sistema tanto às necessidades locais quanto aos requisitos legais de proteção de dados.

* **Nome:** Arthur Nogueira Soares
* **Perfil:** Morador do bairro Mucuripe e Advogado.
* **Justificativa:** Sua inserção na comunidade valida a usabilidade para o público final, enquanto sua formação jurídica oferece uma auditoria crítica sobre a conformidade do sistema (LGPD), essencial para a segurança da instituição.

---

## 2. Metodologia: O Ciclo de Feedback

Para garantir que o software entregue realmente atendesse às necessidades, adotamos um processo de validação em duas etapas, permitindo a correção e o refinamento da solução:

### Etapa 1: Validação Conceitual (Diagnóstico)
* **Data:** 22/11/2025
* **Formato:** Videoconferência via Google Meet.
* **Técnica:** Entrevista com Demonstração Guiada (*Walkthrough*). O entrevistador compartilhou a tela dos protótipos e navegou pelo sistema, solicitando ao usuário que descrevesse suas impressões e dúvidas.
* **Resultado:** Identificação de falhas críticas na coleta de dados (LGPD), na clareza do status dos livros e na falta de informações de acessibilidade.

### Etapa 2: Homologação da Solução (Entrega Final)
* **Data:** 01/12/2025
* **Foco:** Apresentação do **software funcional (rodando em produção)** para verificar se as correções foram efetivas.
* **Técnica:** *Live Demo* via Google Meet, onde o usuário testou as funcionalidades corrigidas em tempo real.

*As evidências (Termo de Autorização e fotos das reuniões) encontram-se na pasta `validation/evidence/`.*

---

## 3. Matriz de Feedback, Solução e Homologação

Abaixo, detalhamos os pontos críticos levantados na primeira etapa, as soluções técnicas implementadas e o veredito final do usuário.

### 🔴 Ponto Crítico 1: Transparência e LGPD
* **O Problema (Diagnóstico - 22/11):** O usuário alertou que o sistema pedia dados sensíveis (endereço) sem um termo de consentimento explícito. Comentário: *"Como advogado, sinto falta de um 'li e concordo'. Sem isso, a biblioteca corre risco jurídico."*
* **A Solução Implementada:**
    * **Funcional:** Inclusão de um *checkbox* obrigatório **"Li e concordo com os termos"** no formulário de cadastro.
    * **Técnica:** O backend (`app.py`) foi programado para rejeitar o registro se este campo não for marcado.
* **Veredito na Homologação (01/12):**
    > *"Agora o fluxo está seguro. A exigência do aceite protege a biblioteca de problemas futuros com a lei de dados."* — Arthur Soares (Aprovado ✅)

### 🟡 Ponto de Atenção 2: Clareza de Disponibilidade
* **O Problema (Diagnóstico - 22/11):** O usuário relatou dificuldade em saber se o livro estava na estante apenas lendo a lista textual. Comentário: *"Olhando para 'Dom Casmurro', eu não sei se ele está na estante agora ou se o vizinho pegou."*
* **A Solução Implementada:**
    * **Funcional:** Criação de indicadores visuais (Badges) nos cards dos livros: **Verde** para Disponível e **Vermelho** para Emprestado.
    * **Técnica:** Lógica no template (`livros.html`) que renderiza a classe CSS correta baseada no status do banco de dados.
* **Veredito na Homologação (01/12):**
    > *"A visualização ficou intuitiva. As cores ajudam a identificar rápido o que posso pegar emprestado sem perder a viagem."* — Arthur Soares (Aprovado ✅)

### 🔵 Melhoria de Inclusão 3: Acessibilidade nos Eventos
* **O Problema (Diagnóstico - 22/11):** Falta de informações sobre acessibilidade física para idosos nos locais dos eventos. Comentário: *"Moro aqui no Mucuripe e é difícil saber onde ficam as salas. Seria ótimo saber se tem acessibilidade."*
* **A Solução Implementada:**
    * **Funcional:** Adição do campo "Local Acessível" na agenda cultural, com destaque visual na interface.
    * **Técnica:** Alteração no esquema do banco de dados e no formulário de criação de eventos para suportar e exibir essa informação.
* **Veredito na Homologação (01/12):**
    > *"Essencial para a nossa comunidade no Mucuripe, que tem muitos idosos."* — Arthur Soares (Aprovado ✅)

---

## 4. Conclusão

O sistema foi considerado **homologado** pelo representante do público-alvo. A estratégia de realizar uma segunda rodada de validação com o software pronto provou-se eficaz, garantindo que a entrega final não fosse apenas um código funcional, mas uma ferramenta ajustada às necessidades reais, legais e sociais da comunidade.

O sistema final é significativamente mais **seguro**, **transparente** e **inclusivo** do que a versão planejada inicialmente.
