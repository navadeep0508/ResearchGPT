from sqlalchemy import Column,Integer,String
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