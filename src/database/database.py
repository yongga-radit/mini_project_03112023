import sqlalchemy as _sa
import sqlalchemy.ext.declarative as _declare
import sqlalchemy.orm as _orm

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://user:password@localhost/database_minipro27112023.db"

engine = _sa.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = _orm.sessionmaker(autocommit=False, 
                                 autoflush=False, 
                                 bind=engine
                                 )

Base = _declare.declarative_base()


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db():
    data = SessionLocal()
    try:
        yield data
    except Exception as e:
        data.rollback()
        raise e
    finally:
        data.close()