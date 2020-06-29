import sqlalchemy as db
import os

class MapperConnection:
    __engine = None

    def __new__(cls, val="Normal"):
        if MapperConnection.__engine is None:
            dbtype, dbuser, dbname = MapperConnection.get_connection_settings(val)
            MapperConnection.__engine = db.create_engine(("{dbtype}://{dbuser}:" + os.environ["PSQL_PASSWORD"] + "@{dbname}").format(
            dbtype=dbtype, dbuser=dbuser, dbname=dbname
        ))
        return MapperConnection.__engine

    @classmethod
    def get_connection_settings(cls, val):
        dbtype="postgresql+psycopg2"
        dbuser="asset_manager"
        dbname="localhost/asset_management" if val=="Normal" else "localhost/asset_management_test_db"
        return dbtype, dbuser, dbname
