# Gitrics

> Uma plataforma de análise de repositórios GitHub que transforma dados de desenvolvimento em métricas e insights acionáveis.

## 📚 Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Configuração do banco de dados](#configuração-do-banco-de-dados)
- [Como executar](#como-executar)
- [Testes](#testes)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Tecnologias](#tecnologias)
- [Documentação](#documentação)

## 📖 Sobre o projeto

O **Gitrics** é uma plataforma desenvolvida para transformar dados de repositórios do GitHub em métricas e visualizações, permitindo acompanhar informações relevantes sobre o desenvolvimento e obter insights para melhorar o fluxo de trabalho e as entregas.

## ✨ Funcionalidades

* [x] 🔗 Integração com o GitHub
* [] 📊 Coleta e análise de dados de repositórios
* [ ] 📈 Dashboard de métricas de desenvolvimento
* [ ] 🔀 Análise de Pull Requests

  * [ ] Tempo médio até a aprovação
  * [ ] Tempo médio até o merge
  * [ ] Pull Requests abertos e fechados
  * [ ] Taxa de aprovação
* [ ] 💻 Análise de commits

  * [ ] Frequência de commits
  * [ ] Distribuição de commits por período
  * [ ] Contribuições por desenvolvedor
  * [ ] Evolução das contribuições
* [ ] 📝 Análise de Issues

  * [ ] Issues abertas e fechadas
  * [ ] Tempo médio de resolução
  * [ ] Evolução do backlog
  * [ ] Distribuição por status
* [ ] 👥 Métricas da equipe

  * [ ] Contribuições por membro
  * [ ] Distribuição de trabalho
  * [ ] Evolução da atividade da equipe
  * [ ] Comparação de métricas ao longo do tempo


## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- [Python](https://www.python.org/downloads/) >= 3.12
- [Node.js](https://nodejs.org/en/download) >= 22
- [PostgreSQL](https://www.postgresql.org/download/) >= 18
- [Git](https://git-scm.com/install/)

## 🗄️ Configuração do banco de dados

O Gitrics utiliza **PostgreSQL**. Recomenda-se criar um usuário específico para a aplicação em vez de utilizar diretamente o usuário administrativo `postgres`.

### 1. Criando o usuário

Acesse o PostgreSQL:

```bash
psql -U postgres
```

Crie um usuário para o Gitrics:

```sql
CREATE USER gitrics_user WITH PASSWORD 'sua_senha';
```

### 2. Criando o banco de dados

Crie o banco `gitrics` atribuindo sua propriedade ao usuário da aplicação:

```sql
CREATE DATABASE gitrics OWNER gitrics_user;
```

Conceda os privilégios necessários:

```sql
GRANT ALL PRIVILEGES ON DATABASE gitrics TO gitrics_user;
```

Saia do PostgreSQL:

```sql
\q
```

### 3. Configure as variáveis de ambiente

No arquivo `.env`:

```env
PSGRE_USER="gitrics_user"
PSGRE_PASSWORD="sua_senha"
PSGRE_HOST="localhost"
PSGRE_PORT=5432
PSGRE_DB="gitrics"
```

### 4. Execute as migrations

Com o banco criado e as variáveis configuradas, execute:

```bash
alembic upgrade head
```

O Alembic aplicará automaticamente as migrations pendentes e criará as tabelas necessárias.

> 💡 **Recomendação:** utilize um usuário específico para a aplicação e evite utilizar o usuário administrativo `postgres` nas configurações do Gitrics. Isso reduz os privilégios disponíveis para a aplicação e melhora a segurança do ambiente.


## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/YgorPereira/Gitrics.git
cd Gitrics
```

### 2. Configure as variáveis de ambiente

Acesse o diretório do backend:

```bash
cd server
```

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Configure as variáveis necessárias no arquivo `.env`.

### 3. Configure o backend

Instale o `uv`:

```bash
pip install uv
```

Instale as dependências:

```bash
uv sync
```

Execute as migrações do banco de dados:

```bash
alembic upgrade head
```


Inicie a aplicação:

```bash
 uv run uvicorn app.main:app 
```

> Utilize a flag --reload para rodar em modo de desenvolvimento.

### 4. Execute o frontend

Em outro terminal, acesse o diretório do frontend:

```bash
cd client
```

Instale as dependências:

```bash
npm install
```

Inicie a aplicação:

```bash
npm run dev
```

## ⚙️ Variáveis de ambiente

O backend utiliza variáveis de ambiente para configurar o banco de dados, autenticação com o GitHub e chaves de segurança.

Crie o arquivo `.env` a partir do `.env.example` e preencha os valores necessários.

## 🧪 Testes

O projeto utiliza [Pytest](https://docs.pytest.org/en/stable/) para execução dos testes, separados em **unitários** e **de integração**.

Execute os comandos a partir do diretório `server`:

### Todos os testes

```bash
uv run pytest
```

### Testes unitários

```bash
uv run pytest -m unit
```

### Testes de integração

```bash
uv run pytest -m integration
```

### Exibir detalhes da execução

```bash
uv run pytest -v
```

### Executar um arquivo específico

```bash
uv run pytest tests/auth/unit/test_auth_service.py
```

Os markers utilizados são:

| Marker        | Descrição                                                      |
| ------------- | -------------------------------------------------------------- |
| `unit`        | Testes unitários, focados em componentes isolados              |
| `integration` | Testes de integração entre diferentes componentes da aplicação |


## 🛠️ Tecnologias

### Frontend

- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vite.dev/)
- [Node.js](https://nodejs.org/)

### Backend

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pytest](https://docs.pytest.org/en/stable/)

### Database

- [PostgreSQL](https://www.postgresql.org/)

## 📚 Documentação

- [Autenticação Github OAuth2](./docs/server/github_oauth_flow.md)
