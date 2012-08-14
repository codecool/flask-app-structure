from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, text
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import UserMixin

from .database import Base

bcrypt = Bcrypt()

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    _password = Column('password', String(120), nullable=False)
    creation_date = Column(DateTime, default=text("current_timestamp"))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value)

    def get_id(self):
        return unicode(self.id)
    
    def match_password(self, value):
        return bcrypt.check_password_hash(self._password, value)
    
    def __repr__(self):
        return u"User<%s>" % self.username
