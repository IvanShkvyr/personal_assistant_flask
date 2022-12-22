from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src import db
from src.libs import constants


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(constants.LOGIN_LENGHT), nullable=False)
    phone = db.Column(db.String(constants.PHONE_LENGHT), unique=True, nullable=False)
    hash = db.Column(db.String(constants.HASH_LENGHT), nullable=False)
    token_cookie = db.Column(db.String(constants.HASH_LENGHT), nullable=True, default=None)
    addressbook = relationship("AddressBook", back_populates="user")

    
class AddressBook(db.Model):
    __tablename__ = "addressbook"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(constants.FIRST_NAME_LENGHT), unique=True)
    last_name = db.Column(db.String(constants.LAST_NAME_LENGHT))
    phone = db.Column(db.String(constants.PHONE_LENGHT))
    email = db.Column(db.String(constants.EMAIL_LENGHT))
    address = db.Column(db.String(constants.ADDRESS_LENGHT))
    birthday = db.Column(db.Date)
    black_list = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("Users", cascade="all, delete", back_populates="addressbook")