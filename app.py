from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Topico, Comentario
from schemas import *
from flask_cors import CORS

info = Info(title="Discuta! API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
topico_tag = Tag(name="Tópico", description="Adição ou visualização de tópicos à base")
comentario_tag = Tag(name="Comentário", description="Adição de um comentário à um tópico cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/topico', tags=[topico_tag],
          responses={"200": TopicoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_topico(form: TopicoSchema):
    """Adiciona um novo Tópico à base de dados

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico = Topico(
        titulo=form.titulo,
        texto=form.texto,
        username=form.username)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando topico
        session.add(topico)
        # efetivando a adição de novo tópico na tabela
        session.commit()
        return apresenta_topico(topico), 200

    except IntegrityError as e:
        # a duplicidade do titulo é a provável razão do IntegrityError
        error_msg = "Tópico de mesmo título já existe!"
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo tópico"
        return {"message": error_msg}, 400


@app.get('/topicos', tags=[topico_tag],
         responses={"200": ListagemTopicosSchema, "404": ErrorSchema})
def get_topicos():
    """Faz a busca por todos os tópicos cadastrados

    Retorna uma representação da listagem de tópicos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    topicos = session.query(Topico).all()

    if not topicos:
        # se não há topicos cadastrados
        return {"topicos": []}, 200
    else:
        # retorna a representação de topico
        print(topicos)
        return apresenta_topicos(topicos), 200


@app.get('/topico', tags=[topico_tag],
         responses={"200": TopicoViewSchema, "404": ErrorSchema})
def get_topico(query: TopicoBuscaSchema):
    """Faz a busca por um tópico a partir do título do tópico

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico_titulo = query.titulo
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    topico = session.query(Topico).filter(Topico.titulo == topico_titulo).first()

    if not topico:
        # se o topico não foi encontrado
        error_msg = "Topico não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        # retorna a representação de topico
        return apresenta_topico(topico), 200

@app.post('/comentario', tags=[comentario_tag],
          responses={"200": TopicoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário à um topicos cadastrado na base identificado pelo id

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico_id  = form.topico_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo topico
    topico = session.query(Topico).filter(Topico.id == topico_id).first()

    if not topico:
        # se topico não encontrado
        error_msg = "Topico não encontrado na base :/"
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    username = form.username
    comentario = Comentario(texto, username)

    # adicionando o comentário ao topico
    topico.adiciona_comentario(comentario)
    session.commit()

    # retorna a representação de topico
    return apresenta_topico(topico), 200