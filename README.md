# Discuta!

Uma simples aplicação de fórum de discussões implementado em Flask!

## Pré-requisitos

* python (3.10.18)
* pip (23.0.1)

## Como executar

Após clonar o repositório, criar e ativar um ambiente virtual para o projeto:

```console
# exemplo em bash/zsh
python -m venv .venv
source .venv/bin/activate 
```

Instalar as dependências descritas no arquivo requirements.txt:

```console
pip install -r requirements.txt
```

E executar a API:

```console
flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no browser para verificar a documentação da API em execução.
