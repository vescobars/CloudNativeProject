from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime
from .model import Model, Base
import bcrypt
from datetime import datetime, timedelta
from uuid import uuid4


class User(Model, Base):
    __tablename__ = 'users'

    STATUS = {
        'VERIFIED': 'VERIFICADO',
        'NOT_VERIFIED': 'NO_VERIFICADO'
    }

    username = Column(String)
    email = Column(String)
    phoneNumber = Column(String)
    dni = Column(String)
    fullName = Column(String)
    password = Column(String)
    salt = Column(String)
    token = Column(String)
    status = Column(String)
    expireAt = Column(DateTime)

    def __init__(self, username, email, phoneNumber, dni, fullName, password):
        Model.__init__(self)
        self.username = username
        self.email = email
        self.phoneNumber = phoneNumber
        self.dni = dni
        self.fullName = fullName

        password = password.encode('utf-8')
        salt = bcrypt.gensalt()

        self.password = bcrypt.hashpw(password, salt).decode()
        self.salt = salt.decode()
        self.status = User.STATUS['NOT_VERIFIED']
        self.set_token()

    def set_token(self):
        self.token = uuid4()
        self.expireAt = datetime.now() + timedelta(hours=1)


class UserSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Str()
    phoneNumber = fields.Str()
    dni = fields.Str()
    fullName = fields.Str()
    password = fields.Str()
    salt = fields.Str()
    token = fields.Str()
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()


class CreatedUserJsonSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()


class GeneratedTokenUserJsonSchema(Schema):
    id = fields.UUID()
    token = fields.Str()
    expireAt = fields.DateTime()


class UserJsonSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    email = fields.Str()
    fullName = fields.Str()
    dni = fields.Str()
    phoneNumber = fields.Str()
    status = fields.Str()
