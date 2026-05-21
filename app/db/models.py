from sqlalchemy import Column,Integer,String,JSON,Text
from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)

    username=Column(String,unique=True,index=True)

    password = Column(String)

class ChatHistory(Base):
    __tablename__="chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(String)

    answer = Column(String)

    username = Column(
        String,
        ForeignKey("users.username")
    )

    user = relationship("User")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document = Column(Text)

    embedding = Column(JSON)
