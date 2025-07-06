from pydantic import BaseModel
from typing import List
from model.topico import Topico

from schemas import ComentarioSchema


class TopicoSchema(BaseModel):
    """ Define como um novo tópico a ser inserido deve ser representado
    """
    titulo: str = "Dúvida sobre sqlite"
    texto: str = "Como instalar?"
    username: str = "spongebob"


class TopicoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no título do tópico.
    """
    titulo: str = "Teste"


class ListagemTopicosSchema(BaseModel):
    """ Define como uma listagem de tópicos será retornada.
    """
    topicos:List[TopicoSchema]


def apresenta_topicos(topicos: List[Topico]):
    """ Retorna uma representação do tópico seguindo o schema definido em
        TopicoSchema.
    """
    result = []
    for topico in topicos:
        result.append({
            "id": topico.id,
            "titulo": topico.titulo,
            "username": topico.username,
            "total_comentarios": len(topico.comentarios)
        })

    return {"topicos": result}


class TopicoViewSchema(BaseModel):
    """ Define como um tópico será visualizado: tópico + comentários.
    """
    id: int = 1
    titulo: str = "Dúvida sobre sqlite"
    texto: str = "Como instalar?"
    username: str = "spongebob"
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


def apresenta_topico(topico: Topico):
    """ Retorna uma representação do tópico seguindo o schema definido em
        TopicoViewSchema.
    """
    return {
        "id": topico.id,
        "titulo": topico.titulo,
        "texto": topico.texto,
        "username": topico.username,
        "total_comentarios": len(topico.comentarios),
        "comentarios": [{"texto": c.texto, "username": c.username} for c in topico.comentarios]
    }