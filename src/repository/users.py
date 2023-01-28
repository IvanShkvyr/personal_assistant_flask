import bcrypt

from src.models import Users
from src import db

def create_user(login, phone, password, session_):
    hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10))
    user = Users(login=login, phone=phone, hash=hash)
    session_.add(user)
    session_.commit()
    return user


def login(login, password, session_):
    user = find_by_login(login, session_)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode("utf-8"), user.hash):
        return None
    return user


def find_by_login(login, session_):
    return session_.query(Users).filter(Users.login == login).first()


def set_token(user, token):
    user.token_cookie = token
    db.session.commit()


def get_user_by_token(token_user):
    user = db.session.query(Users).filter(Users.token_cookie == token_user).first()
    if not user:
        return None
    return user
