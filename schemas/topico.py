from pydantic import BaseModel
from typing import Optional, List
from model.topico import Topico

from schemas import ComentarioSchema


class TopicoSchema(BaseModel):
    """ Define como um novo topico a ser inserido deve ser representado
    """
    titulo: str = "Dúvida sobre sqlite"
    texto: str = "Como instalar?"
    username: str = "spongebob"


class TopicoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no titulo do topico.
    """
    titulo: str = "Teste"


class ListagemTopicosSchema(BaseModel):
    """ Define como uma listagem de topicos será retornada.
    """
    topicos:List[TopicoSchema]


def apresenta_topicos(topicos: List[Topico]):
    """ Retorna uma representação do topico seguindo o schema definido em
        TopicoViewSchema.
    """
    result = []
    for topico in topicos:
        result.append({
            "titulo": topico.titulo,
            "texto": topico.texto,
            "username": topico.username,
        })

    return {"topicos": result}


class TopicoViewSchema(BaseModel):
    """ Define como um topico será retornado: topico + comentários.
    """
    id: int = 1
    titulo: str = "Dúvida sobre sqlite"
    texto: str = "Como instalar?"
    username: str = "spongebob"
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


class TopicoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    titulo: str

def apresenta_topico(topico: Topico):
    """ Retorna uma representação do topico seguindo o schema definido em
        TopicoViewSchema.
    """
    return {
        "id": topico.id,
        "titulo": topico.titulo,
        "texto": topico.texto,
        "username": topico.username,
        "total_comentarios": len(topico.comentarios),
        "comentarios": [{"texto": c.texto} for c in topico.comentarios]
    }