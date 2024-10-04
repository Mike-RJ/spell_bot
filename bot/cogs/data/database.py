from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
DATABASE_URLS = {
    'messages' : 'sqlite:///messages.db',
    'actions' : 'sqlite:///actions.db',
    'keywords' : 'sqlite:///keywords.db'
}

# messages_session = sessionmaker(bind=messages_engine)
# actions_session = sessionmaker(bind=actions_engine)
# spells_session = sessionmaker(bind=spells_engine)

class MessageRecord(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, unique=True, nullable=False)
    message_content = Column(Text, nullable=False)
    author_id = Column(Integer, nullable=False)
    author_name = Column(String, nullable=False)
    channel_id = Column(Integer, nullable=False)
    channel_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

class KeyWord(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)

class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

def init_db():
    messages_engine = create_engine(DATABASE_URLS['messages'])
    actions_engine = create_engine(DATABASE_URLS['actions'])
    keywords_engine = create_engine(DATABASE_URLS['keywords'])
    Base.metadata.create_all(bind=messages_engine)
    Base.metadata.create_all(bind=actions_engine)
    Base.metadata.create_all(bind=keywords_engine)
