import os


class Config:
    """Configurações da aplicação"""

    # Configurações do banco de dados
    DB_PATH = "database/"
    DB_URL = f"sqlite:///{DB_PATH}/db.sqlite3"

    # Configurações do SQLite para threading
    SQLITE_CONNECT_ARGS = {"check_same_thread": False}

    # Configurações do Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    DEBUG = True

    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação"""
        # Cria a pasta database se não existir
        if not os.path.exists(Config.DB_PATH):
            os.makedirs(Config.DB_PATH)
