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