from datetime import datetime, timedelta
import uuid

from flask import make_response, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from . import app
from .repository import users


@app.route("/check")
def check():
    return "I am working"

@app.route("/", strict_slashes=False)
def index():
    auth = True if 'login' in session else False
    return render_template("pages/index.html", title="personal asistant", auth=auth)

@app.route("/registration", methods=["GET", "POST"], strict_slashes=False)
def registration():
    auth = True if 'login' in session else False
    if auth:
        return redirect(url_for("index"))
    if request.method == "POST":
        # Перевірка схеми на корекність введених даних
        # НАПИСАТИ

        login = request.form.get("login")
        phone = request.form.get("phone")
        password = request.form.get("password")

        try:
            users.create_user(login, phone, password)
            return redirect(url_for("login"))
        except IntegrityError:
            return render_template("pages/registration.html", messages={'Error': f"User with phone {phone} exist!"})
    return render_template("pages/registration.html")


@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    print(1)
    auth = True if 'login' in session else False
    print(2)
    if request.method == "POST":    
        login = request.form.get("login")
        password = request.form.get("password")
        remember = True if request.form.get("remember") == "on" else False
        user = users.login(login, password)
        if user is None:
            return render_template("pages/login.html", messages={'Error': f"Invalid credentials"})
        session["login"] = {"login": user.login, "id": user.id}
        response = make_response(redirect(url_for("index")))
        if remember:
            token = str(uuid.uuid4())
            expire_data = datetime.now() + timedelta(days=60)
            response.set_cookie('login', token, expires=expire_data)
            users.set_token(user, token)
    
        return response
    if auth:
        return redirect(url_for("index"))
    else:
        return render_template("pages/login.html")
    









