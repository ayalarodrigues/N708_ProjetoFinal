# Arquitetura do Sistema — Biblioteca Comunitária

## 1. Visão Geral

O sistema evoluiu de uma arquitetura baseada em **microserviços** (React + Node API) para uma **Arquitetura Monolítica Modular**, seguindo o padrão **MVT (Model–View–Template)** com o framework **Flask (Python)**.

A mudança foi motivada por:

- Redução da complexidade de manutenção  
- Maior segurança no tráfego de dados (renderização server-side)  
- Agilidade no desenvolvimento e validação com os usuários finais  

---

## 2. Diagrama de Arquitetura

O diagrama abaixo ilustra o fluxo de dados na arquitetura MVT adotada:

```mermaid
graph TD
    subgraph "Cliente (Navegador)"
        A[Browser / Mobile]
    end

    subgraph "Servidor (Python/Flask)"
        B[Controller / Rotas - app.py]
        C[Template Engine - Jinja2]
        D[ORM / Modelagem de Dados]
    end

    subgraph "Persistência"
        E[(Banco de Dados SQLite)]
    end

    %% Fluxo de Dados
    A -- "1. Requisição HTTP (GET/POST)" --> B
    B -- "2. Processa Lógica" --> D
    D -- "3. Consulta / Grava" --> E
    E -- "4. Retorna Dados" --> D
    D -- "5. Envia Objetos" --> B
    B -- "6. Injeta Dados no Template" --> C
    C -- "7. Renderiza HTML" --> B
    B -- "8. Resposta HTML/CSS" --> A

````
## 3. Tecnologias Selecionadas

- **Linguagem:** Python 3.10+ — Alta legibilidade e robustez.
- **Framework Web:** Flask — Microframework flexível.
- **Frontend:** HTML5, CSS3 (Bootstrap 5 via CDN) e Jinja2.
- **Banco de Dados:** SQLite — Nativo, serverless, ideal para a escala de bibliotecas comunitárias.
- **Hospedagem:** Preparado para deploy em contêineres ou serviços como Render/PythonAnywhere.

---

## 4. Justificativa de Mudanças  
*(Relação N705 → N708)*

Conforme permitido no edital da disciplina, ocorreram ajustes arquiteturais justificados por:

### Segurança e LGPD  
O tratamento de sessões e dados sensíveis no lado do servidor (Server-Side) simplificou a conformidade com a LGPD, um requisito identificado durante a avaliação jurídica.

### Interoperabilidade  
O uso de SQLite elimina a necessidade de instalação de servidores de banco complexos (como PostgreSQL) nas máquinas das bibliotecas comunitárias, que geralmente possuem hardware limitado.

### Manutenibilidade  
Unificar Frontend e Backend em uma única linguagem (Python) facilita a transferência de conhecimento para futuros mantenedores voluntários do projeto.
 
Unificar frontend e backend em Python reduz a curva de aprendizagem e facilita a continuidade por voluntários e futuros desenvolvedores.

