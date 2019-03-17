from mongoengine import connect
from app.config import Config

class Database:
    __db = None

    @classmethod
    def get_connection(connection):
        config = Config()
        config = config.get_config()
        if connection.__db is None:
            connection.__db = connect(config['mongodb']['db'],
                host=config['mongodb']['host'],
                port=config['mongodb']['port'])
        return connection.__db
