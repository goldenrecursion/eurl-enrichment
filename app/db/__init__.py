import os 

from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = os.environ['POSTGRES_CONNECTION_URL'] if os.environ.get('POSTGRES_CONNECTION_URL') else 'sqlite:///:memory:'
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()


class FeedList(Base):
    __tablename__ = 'feed_list'

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    list_name = Column(String)
    PrimaryKeyConstraint('source', 'list_name', name='source_list')


class FeedRunTime(Base):
    __tablename__ = 'feed_runtime'

    source = Column(String, primary_key=True, index=True)
    last_runtime = Column(Integer)
    last_starttime = Column(Integer)
    processed = Column(Integer)


def add_feedlist(source: str, list_name: str) -> FeedList:
    return add_db_entry(FeedList(source=source, list_name=list_name))


def add_db_entry(object: any) -> any:
    try:
        db.add(object)
        db.commit()
        db.refresh(object)
        return object
    except:
        db.flush()
        db.rollback()
        return False 


def feedlist_entry_exist(source: str, list_name: str, table='feedlist') -> FeedList:
    data = db.query(FeedList).filter_by(source=source, list_name=list_name).first()

    if data:
        return data
    else:
        return False


Base.metadata.create_all(bind=engine)

