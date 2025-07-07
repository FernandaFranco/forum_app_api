from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from model import Base


class Comentario(Base):
    __tablename__ = "comentario"

    id = Column(Integer, primary_key=True)
    texto = Column(String(3000))
    username = Column(String(20))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e seu tópico.
    topico = Column(Integer, ForeignKey("topico.pk_topico"), nullable=False)

    def __init__(
        self, texto: str, username: str, data_insercao: Union[DateTime, None] = None
    ):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            username: o nome de usuário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base.
        """
        self.texto = texto
        self.username = username
        if data_insercao:
            self.data_insercao = data_insercao
