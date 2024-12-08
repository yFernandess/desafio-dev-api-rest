[![Python application](https://github.com/yFernandess/desafio-dev-api-rest/actions/workflows/python-app.yml/badge.svg)](https://github.com/yFernandess/desafio-dev-api-rest/actions/workflows/python-app.yml)

# Desafio Dev API REST

Este é um projeto de API REST para gerenciamento de contas bancárias.

O projeto foi desenvolvido utilizando a linguagem Python na versão 3.11 com o framework FastAPI.
Foi utilizado o padrão de projeto MVC na implementação dessa API.
Para instruções de banco de dados foi utilizado a lib peewee (ORM) com o banco de dados SQLite criado em tempo de execução.
Para os testes unitário foi utilizado a lib pytest onde foi coberta a camada de service da aplicação e foi criado uma Action no github para a execução desses testes automatizados.
Criado também um dockerfile para a execução da API em containers.



## Requisitos

- Python 3.11
- Docker (opcional)

### Clonar o Repositório

```sh
git clone https://github.com/yFernandess/desafio-dev-api-rest.git
cd desafio-dev-api-rest
```
## Instalação Local

```sh
pip install -r requirements.txt
```

```sh
python app/http_server.py
```

## Instalação via Docker

```sh
docker build -t core-accounts .
```

```sh
docker run -p 8000:8000 core-accounts
```

## Executando a Aplicação via Swagger
[http://localhost:8000/docs](http://localhost:8000/docs)


## Estrutura do Projeto

A estrutura de diretórios e arquivos do projeto é a seguinte:

```
desafio-dev-api-rest/
.
├── app
│   ├── config
│   │   ├── __init__.py
│   │   ├── enums
│   │   │   ├── account.py
│   │   ├── exceptions
│   │   │   ├── general.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── account.py
│   │   │   ├── account_owner.py
│   │   │   ├── transaction.py
│   │   ├── repositories
│   │   │   ├── account_repository.py
│   │   │   ├── account_owner_repository.py
│   │   │   ├── transaction_repository.py
│   │   ├── provider.py
│   ├── handlers
│   │   ├── http
│   │   │   ├── account_handler.py
│   │   │   ├── transaction_handler.py
│   ├── interfaces
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── account_owner.py
│   │   ├── transaction.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   ├── http_server.py
├── tests
│   ├── unit
│   │   ├── services
│   │   │   ├── test_account_service.py
│   │   │   ├── test_transaction_service.py
├── Dockerfile
├── requirements.txt
├── README.md
```

## Endpoints da API

### 1. Gerenciamento de Contas

#### Criar Conta
- **URL:** `/accounts`
- **Método:** `POST`
- **Descrição:** Cria uma nova conta bancária.
  ```

#### Obter Conta
- **URL:** `/accounts/{account_id}`
- **Método:** `GET`
- **Descrição:** Obtém os detalhes de uma conta bancária específica.
  ```

### 2. Gerenciamento de Transações

#### Criar Transação
- **URL:** `/transactions`
- **Método:** `POST`
- **Descrição:** Cria uma nova transação para uma conta bancária.
  ```

#### Obter Transações
- **URL:** `/accounts/{account_id}/transactions`
- **Método:** `GET`
- **Descrição:** Obtém todas as transações de uma conta bancária específica.
  ```

### 3. Gerenciamento de Proprietários de Contas

#### Criar Proprietário de Conta
- **URL:** `/account_owners`
- **Método:** `POST`
- **Descrição:** Cria um novo proprietário de conta.
  ```

#### Obter Proprietário de Conta
- **URL:** `/account_owners/{account_owner_id}`
- **Método:** `GET`
- **Descrição:** Obtém os detalhes de um proprietário de conta específico.
  ```