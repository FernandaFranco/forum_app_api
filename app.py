from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Topico, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Forum API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
topico_tag = Tag(name="Topico", description="Adição, visualização e remoção de topicos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um topico cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/topico', tags=[topico_tag],
          responses={"200": TopicoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_topico(form: TopicoSchema):
    """Adiciona um novo Topico à base de dados

    Retorna uma representação dos topicos e comentários associados.
    """
    topico = Topico(
        titulo=form.titulo,
        texto=form.texto,
        username=form.username)
    logger.debug(f"Adicionando topico de titulo: '{topico.titulo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando topico
        session.add(topico)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado topico de titulo: '{topico.titulo}'")
        return apresenta_topico(topico), 200

    except IntegrityError as e:
        # como a duplicidade do titulo é a provável razão do IntegrityError
        error_msg = "Topico de mesmo titulo já salvo na base :/"
        logger.warning(f"Erro ao adicionar topico '{topico.titulo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar topico '{topico.titulo}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/topicos', tags=[topico_tag],
         responses={"200": ListagemTopicosSchema, "404": ErrorSchema})
def get_topicos():
    """Faz a busca por todos os Topico cadastrados

    Retorna uma representação da listagem de topicos.
    """
    logger.debug(f"Coletando topicos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    topicos = session.query(Topico).all()

    if not topicos:
        # se não há topicos cadastrados
        return {"topicos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(topicos))
        # retorna a representação de topico
        print(topicos)
        return apresenta_topicos(topicos), 200


@app.get('/topico', tags=[topico_tag],
         responses={"200": TopicoViewSchema, "404": ErrorSchema})
def get_topico(query: TopicoBuscaSchema):
    """Faz a busca por um Topico a partir do id do topico

    Retorna uma representação dos topicos e comentários associados.
    """
    topico_titulo = query.titulo
    logger.debug(f"Coletando dados sobre topico #{topico_titulo}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    topico = session.query(Topico).filter(Topico.titulo == topico_titulo).first()

    if not topico:
        # se o topico não foi encontrado
        error_msg = "Topico não encontrado na base :/"
        logger.warning(f"Erro ao buscar topico '{topico_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Topico econtrado: '{topico.titulo}'")
        # retorna a representação de topico
        return apresenta_topico(topico), 200


@app.delete('/topico', tags=[topico_tag],
            responses={"200": TopicoDelSchema, "404": ErrorSchema})
def del_topico(query: TopicoBuscaSchema):
    """Deleta um Topico a partir do titulo de topico informado

    Retorna uma mensagem de confirmação da remoção.
    """
    topico_titulo = unquote(unquote(query.titulo))
    print(topico_titulo)
    logger.debug(f"Deletando dados sobre topico #{topico_titulo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Topico).filter(Topico.titulo == topico_titulo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado topico #{topico_titulo}")
        return {"mesage": "Topico removido", "id": topico_titulo}
    else:
        # se o topico não foi encontrado
        error_msg = "Topico não encontrado na base :/"
        logger.warning(f"Erro ao deletar topico #'{topico_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": TopicoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um topicos cadastrado na base identificado pelo id

    Retorna uma representação dos topicos e comentários associados.
    """
    topico_id  = form.topico_id
    logger.debug(f"Adicionando comentários ao topico #{topico_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo topico
    topico = session.query(Topico).filter(Topico.id == topico_id).first()

    if not topico:
        # se topico não encontrado
        error_msg = "Topico não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao topico '{topico_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao topico
    topico.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao topico #{topico_id}")

    # retorna a representação de topico
    return apresenta_topico(topico), 200