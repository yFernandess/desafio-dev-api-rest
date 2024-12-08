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
│   │   │   ├── transaction.py
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
│   │   ├── exceptions.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   ├── http_server.py
├── unit_tests
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

#### Criar um proprietário de uma conta
- **URL:** `/owner`
- **Método:** `POST`
- **Descrição:** Cria um proprietário de uma conta bancária.

#### Excluir um proprietário de uma conta
- **URL:** `/owner/{cpf}`
- **Método:** `DELETE`
- **Descrição:** Exclui um proprietário de uma conta bancária.

#### Criar uma nova conta
- **URL:** `/create`
- **Método:** `POST`
- **Descrição:** Cria uma nova conta bancária vinculada ao proprietário.

#### Obter Conta
- **URL:** `/accounts/{account_id}`
- **Método:** `GET`
- **Descrição:** Obtém os detalhes de uma conta bancária específica.

#### Bloquear uma conta
- **URL:** `/block`
- **Método:** `POST`
- **Descrição:** Bloqueia uma conta bancária vinculada ao proprietário.

#### Desbloquear uma conta
- **URL:** `/unblock`
- **Método:** `POST`
- **Descrição:** Desbloqueia uma conta bancária vinculada ao proprietário.

#### Fechar uma conta
- **URL:** `/close`
- **Método:** `POST`
- **Descrição:** Encerra uma conta bancária vinculada ao proprietário.

### 2. Gerenciamento de Transações

#### Buscar extrato bancário por período
- **URL:** `/statement/{account_id}`
- **Método:** `GET`
- **Descrição:** Busca as transações de uma conta por período.

#### Realizar um depósito bancário
- **URL:** `/deposit`
- **Método:** `POST`
- **Descrição:** Realiza um depósito em uma conta bancária específica.

#### Realizar um saque bancário
- **URL:** `/withdraw`
- **Método:** `POST`
- **Descrição:** Realiza um saque em uma conta bancária específica.