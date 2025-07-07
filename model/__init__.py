import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

# Importando configurações
from config import Config

# importando os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.topico import Topico

# Cria a pasta database se não existir
if not os.path.exists(Config.DB_PATH):
    os.makedirs(Config.DB_PATH)

engine = create_engine(
    Config.DB_URL, echo=False, connect_args=Config.SQLITE_CONNECT_ARGS
)

# Instancia um criador de seção com o banco
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Cria o banco se não existir
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
