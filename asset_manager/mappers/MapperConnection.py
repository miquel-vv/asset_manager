import sqlalchemy as db

class MapperConnection:
    def __init__(self):
        dbtype, dbuser, dbname = self.get_connection_settings()
        self.engine = db.engine("{dbtype}://{dbuser}:" + os.environ["PSQL_PASSWORD"] + "@{dbname}".format(
            dbtype, dbuser, dbname
        ))

    def get_connection_settings(self):
        dbtype="postgresql+psycopg2"
        dbuser="asset_manager"
        dbname="@localhost/asset_management"
        return dbtype, dbuser, dbname

    def get_engine(self):
        return self.engine