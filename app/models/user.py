#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.insert(0,'../../')

from sqlalchemy import Column, String ,Integer,ForeignKey,Table
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import *

__all__ = ['Authority', 'Group', 'User',  'Session','init_db']

association_table = Table('associations', Base.metadata,
    Column('auth_id', Integer, ForeignKey('authority.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)
class Authority(Base):
        __table_args__ = {'extend_existing': True}
        __tablename__ = 'authority'
        id = Column(Integer,primary_key=True)
        name = Column(String)
        
        def __init__(self, name):
                self.name = name
                
class Group(Base):
        __table_args__ = {'extend_existing': True}
        __tablename__ = 'group'
        id = Column(Integer,primary_key=True)
        name = Column(String(10),unique=True)
        auths = relationship("Authority",secondary=association_table,
                             backref="groups")
        
        users = relationship("User",backref="groups")
        
        def __init__(self, name):
            self.name = name
        
class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        username = Column(String)
        email = Column(String)
        password = Column(String)
        group_id = Column(Integer, ForeignKey('group.id'))
        session = relationship("Session", uselist=False,
                               backref='user')
        
        def __init__(self,  username,  email, password, group):
                self.username = username
                self.email = email
                self.password = password
                self.group = group

import hmac
from hashlib import sha1, md5
SECRET_KEY = 'sdfsdfasdfjklasdfn sl'

def _secret_key(key=None):
    if key is None:
        key = SECRET_KEY

    if isinstance(key, unicode):  # pragma: no cover
        key = key.encode('latin1')  # ensure bytes

    return key


def make_secure_token(*args):
    '''
    This will create a secure token that you can use as an authentication
    token for your users. It uses heavy-duty HMAC encryption to prevent people
    from guessing the information. (To make it even more effective, if you
    will never need to regenerate the token, you can  pass some random data
    as one of the arguments.)

    :param \*args: The data to include in the token.
    :type args: args
    :param \*\*options: To manually specify a secret key, pass ``key=THE_KEY``.
        Otherwise, the ``current_app`` secret key will be used.
    :type \*\*options: kwargs
    '''
    key = SECRET_KEY
    key = _secret_key(key)

    l = [s if isinstance(s, bytes) else s.encode('utf-8') for s in args]

    payload = b'\0'.join(l)

    token_value = hmac.new(key, payload, sha1).hexdigest()

    if hasattr(token_value, 'decode'):  # pragma: no cover
        token_value = token_value.decode('utf-8')  # ensure bytes

    return token_value


class Session(Base):
        __tablename__ = 'session'
        id = Column(Integer, primary_key = True)
        token = Column(String,unique=True)
        expires_in = Column(DateTime)
        user_id = Column(Integer, ForeignKey('user.id'))
        
        def __init__(self,expires_in,user,pwd):
                self.expires_in = expires_in
                self.token = make_secure_token(user,pwd)
                # @AssociationType server.apiapp.models.User


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
    auth_user = Authority('user')
    db_session.add(auth_user)
    db_session.commit()
    group_user = Group('user')
    group_user.auths = [auth_user,]

    db_session.add(group_user)
    db_session.commit()
    
    
    

if __name__ == '__main__':
    init_db()
