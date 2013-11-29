#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.insert(0,'../../')

from sqlalchemy import Column, String ,Integer,ForeignKey,Table
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

__all__ = ['Authority', 'Group', 'User',  'Session']

association_table = Table('association', Base.metadata,
    Column('auth_id', Integer, ForeignKey('authority.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)
class Authority(Base):
        __tablename__ = 'authority'
        id = Column(Integer,primary_key=True)
        name = Column(String)
        
        def __init__(self):
                self.___string_name = None
                self.___attribute = None
                self._unnamed_Group_ = None
                # @AssociationType server.apiapp.models.Group
                
class Group(Base):
        __tablename__ = 'group'
        id = Column(Integer,primary_key=True)
        name = Column(String(10), primary_key=True)
        auths = relationship("Authority",secondary=association_table,
                             backref="groups")
        
        users = relationship("User",backref="groups")
        


class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        username = Column(String)
        email = Column(String)
        group_id = Column(Integer, ForeignKey('group.id'))
        session = relationship("Session", uselist=False,
                               backref='user')
        
        def __init__(self):
                self.___string_username = None
                self.___string_password = None
                self.___string_registerDate = None
                self.___string_sex = None
                self.___string_email = None
                self.___group = None
                self._unnamed_Group_ = None
                # @AssociationType server.apiapp.models.Group
                # @AssociationKind Aggregation
                self._unnamed_Session_ = None
                # @AssociationType server.apiapp.models.Session

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
        token = Column(String,primary_key = True)
        expires_in = Column(DateTime)
        user_id = Column(Integer, ForeignKey('user.id'))
        
        def __init__(self,expires_in,user,pwd):
                self.expires_in = expires_in
                self.token = make_secure_token(user,pwd)
                # @AssociationType server.apiapp.models.User

