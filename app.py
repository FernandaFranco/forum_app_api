from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from sqlalchemy.exc import IntegrityError

from config import Config
from model import Comentario, Session, Topico
from schemas import *

info = Info(title="Discuta! API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

Config.init_app(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
topico_tag = Tag(name="Tópico", description="Adição ou visualização de tópicos na base")
comentario_tag = Tag(
    name="Comentário",
    description="Adição de um comentário a um tópico cadastrado na base",
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove a sessão ao final de cada requisição"""
    Session.remove()


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


@app.post(
    "/topico",
    tags=[topico_tag],
    responses={"200": TopicoViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_topico(form: TopicoSchema):
    """Adiciona um novo tópico à base de dados.

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico = Topico(titulo=form.titulo, texto=form.texto, username=form.username)
    session = Session()
    try:
        session.add(topico)
        session.commit()

        return apresenta_topico(topico), 200

    except IntegrityError as e:
        # Título deve ser único
        error_msg = "Tópico de mesmo título já existe!"
        return {"message": error_msg}, 409

    except Exception as e:
        # Caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo tópico!"
        return {"message": error_msg}, 400
    finally:
        session.close()


@app.get(
    "/topicos",
    tags=[topico_tag],
    responses={"200": ListagemTopicosSchema, "404": ErrorSchema},
)
def get_topicos():
    """Faz a busca por todos os tópicos cadastrados.

    Retorna uma representação da listagem de tópicos.
    """

    session = Session()
    try:
        topicos = session.query(Topico).all()

        if not topicos:
            return {"topicos": []}, 200
        else:
            return apresenta_topicos(topicos), 200
    finally:
        session.close()


@app.get(
    "/topico",
    tags=[topico_tag],
    responses={"200": TopicoViewSchema, "404": ErrorSchema},
)
def get_topico(query: TopicoBuscaSchema):
    """Faz a busca por um tópico a partir do título do tópico.

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico_titulo = query.titulo
    session = Session()
    try:
        topico = session.query(Topico).filter(Topico.titulo == topico_titulo).first()

        if not topico:
            error_msg = "Tópico não encontrado na base!"
            return {"message": error_msg}, 404
        else:
            return apresenta_topico(topico), 200
    finally:
        session.close()


@app.post(
    "/comentario",
    tags=[comentario_tag],
    responses={"200": TopicoViewSchema, "404": ErrorSchema},
)
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário à um topicos cadastrado na base identificado pelo id

    Retorna uma representação dos tópicos e comentários associados.
    """
    topico_id = form.topico_id
    session = Session()
    try:
        topico = session.query(Topico).filter(Topico.id == topico_id).first()

        if not topico:
            error_msg = "Tópico não encontrado na base!"
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
    finally:
        session.close()
