from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Topico(Base):
    __tablename__ = 'topico'

    id = Column("pk_topico", Integer, primary_key=True)
    titulo = Column(String(150), unique=True)
    texto = Column(String(3000))
    username = Column(String(20))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o topico e o comentário.
    # Essa relação é implicita, não está salva na tabela 'topico',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, titulo:str, texto:str, username:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um tópico

        Arguments:
            titulo: título do tópico.
            texto: texto do corpo do tópico
            username: username do criador do tópico
            data_insercao: data de quando o tópico foi inserido à base
        """
        self.titulo = titulo
        self.texto = texto
        self.username = username

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao tópico
        """
        self.comentarios.append(comentario)
