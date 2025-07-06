import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# importando os elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.topico import Topico

db_path = "database/"
# Cria a pasta database se não existir
if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = "sqlite:///%s/db.sqlite3" % db_path

engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se não existir
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
