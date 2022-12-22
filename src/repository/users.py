from src import db
from src import models
import bcrypt


def create_user(login, phone, password):
    hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10))
    user = models.Users(login=login, phone=phone, hash=hash)
    db.session.add(user)
    db.session.commit()
    return user


def login(login, password):
    user = find_by_login(login)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode("utf-8"), user.hash):
        return None
    return user


def find_by_login(login):
    return db.session.query(models.Users).filter(models.Users.login == login).first()


def set_token(user, token):
    user.token_cookie = token
    db.session.commit()


def get_user_by_token(token_user):
    user = db.session.query(models.Users).filter(models.Users.token_cookie == token_user).first()
    if not user:
        return None
    return user
