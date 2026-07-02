# Sistema de Estoque

Este projeto é uma aplicação de gerenciamento de estoque, utilizando containers Docker para isolamento e orquestração. O sistema implementa autenticação baseada em perfis (Admin e Usuário) e persistência de dados.

## Tecnologias Utilizadas

* **Frontend:** HTML5, CSS3 (Mobile-first, Flexbox) e JavaScript assíncrono (Fetch API).
* **Backend:** Python com FastAPI.
* **Banco de Dados:** PostgreSQL 15.
* **Infraestrutura:** Docker e Docker Compose.

## Funcionalidades Principais

* **Autenticação:** Sistema de login com validação de credenciais via banco de dados.
* **Segurança Baseada em Perfis (RBAC):**
    * **Administrador:** Acesso total (Cadastrar produtos, excluir itens do estoque).
    * **Usuário Comum:** Acesso limitado (Visualizar produtos e realizar compras).
* **Gestão de Estoque:** Validação de quantidade (não permite estoque negativo) e atualização em tempo real via banco de dados.
* **Responsividade:** Interface adaptada para dispositivos móveis e desktop.

## Como Executar o Projeto

Certifique-se de ter o **Docker** e o **Docker Compose** instalados.

1. Clone o repositório ou baixe os arquivos.
2. Na raiz do projeto, execute o comando para construir e iniciar os containers:
   ```bash
   docker compose up -d --build