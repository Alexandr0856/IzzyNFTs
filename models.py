from sqlalchemy import Column, String, Integer, BOOLEAN, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///main.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    admin = Column(BOOLEAN)
    wallet = relationship('Wallet', back_populates='user')

    def __init__(self, id, name, admin=False):
        self.id = id
        self.name = name
        self.admin = admin


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    chain = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='wallet')

    def __init__(self, address, chain, user_id, name):
        self.address = address
        self.chain = chain
        self.user_id = user_id
        self.name = name
