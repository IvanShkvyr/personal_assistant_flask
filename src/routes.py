from datetime import datetime, timedelta
import uuid

from flask import flash, make_response, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from . import app
from .repository import users, records
from src import models
from src import db



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

        login = request.form.get("login")
        phone = request.form.get("phone")
        password = request.form.get("password")

        session_ = db.session

        try:
            users.create_user(login, phone, password, session_)
            return redirect(url_for("login"))
        except IntegrityError:
            return render_template("pages/registration.html", messages={'Error': f"User with phone {phone} exist!"}, auth=auth)
    return render_template("pages/registration.html", auth=auth)


@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    auth = True if 'login' in session else False
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        remember = True if request.form.get("remember") == "on" else False
        session_ = db.session
        user = users.login(login, password, session_)
        if user is None:
            return render_template("pages/login.html", messages={'Error': f"Invalid credentials"}, auth=auth)
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
        return render_template("pages/login.html", auth=auth)


@app.route("/logout", strict_slashes=False)
def logout():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))
    session.pop("login")
    response = make_response(redirect(url_for("index")))
    response.set_cookie("login", "", expires=-1)
    return response


@app.route("/create", methods=["GET", "POST"], strict_slashes=False)
def create():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        birthday = request.form.get("birthday")
        black_list = request.form.get("black_list")
        user_id = session["login"]["id"]
        session_ = db.session

        try:
            records.create_record(
                                first_name=first_name,
                                phone=phone,
                                user_id=user_id,
                                last_name=last_name,
                                email=email,
                                address=address,
                                black_list=black_list,
                                birthday=birthday,
                                session_=session_
                                )
        except IntegrityError:
            return render_template("pages/create.html", messages={'Error': f"Record with name {first_name} exist!"}, auth=auth)

        return redirect(url_for("create"))

    return render_template("pages/create.html", auth=auth, users2=session["login"]["login"])


@app.route("/update", methods=["GET", "POST"], strict_slashes=False)
def update():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))
    if request.method == "POST":
        record_id = request.form.get("record_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        birthday = request.form.get("birthday")
        black_list = request.form.get("black_list")
        user_id = session["login"]["id"]
        session_ = db.session
        
        try:
            records.update_record(
                                record_id=record_id,
                                first_name=first_name,
                                phone=phone,
                                user_id=user_id,
                                last_name=last_name,
                                email=email,
                                address=address,
                                black_list=black_list,
                                birthday=birthday,
                                session_=session_
                                )
        except:
            return render_template("pages/update.html", messages={'Error': f"Record with id {record_id} does not exist!"}, auth=auth)

        return redirect(url_for("update"))

    return render_template("pages/update.html", auth=auth, users2=session["login"]["login"])


@app.route("/remove", methods=["GET", "POST"], strict_slashes=False)
def remove():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))

    if request.method == "POST":
        record_id = request.form.get("record_id")
        user_id = session["login"]["id"]
        result_is = records.delete_record(record_id, user_id)
        if result_is:
            flash("Deleted successfully!")
        else:
            flash("The user does not have such an entry in the address book")
    return render_template("pages/remove.html", auth=auth, users2=session["login"]["login"])


@app.route("/show_record", methods=["GET", "POST"], strict_slashes=False)
def show_record():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))
    if request.method == "POST":
        record_id = request.form.get("record_id")
        user_id = session["login"]["id"]
        session_ = db.session

        result = records.get_record_user(record_id, user_id, session_)

        if not result:
            flash("The user does not have such an entry in the address book")
        else:
            message = "{:^3};{:^10};{:^10};{:^20};{:^30};{:^70};{:^12};{:^12}".format(result.id, result.first_name, result.last_name, result.phone,
                                                                             result.email, result.address, result.birthday.strftime('%d %B %Y'),
                                                                             result.black_list)
            flash(message)
    return render_template("pages/show_record.html", auth=auth, users2=session["login"]["login"])


@app.route("/show_all", methods=["GET", "POST"], strict_slashes=False)
def show_all():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))

    if request.method == "POST":
        user_id = session["login"]["id"]
        results = records.show_all_records(user_id)
        if not results:
            flash("The user does not have such an entry in the address book")

        for result in results:
            message = "{:^3};{:^10};{:^10};{:^20};{:^30};{:^70};{:^12};{:^12}".format(result.id, result.first_name, result.last_name, result.phone,
                                                                             result.email, result.address, result.birthday.strftime('%d %B %Y'),
                                                                             result.black_list)
            flash(message)  

    return render_template("pages/show_all.html", auth=auth, users2=session["login"]["login"])


@app.route("/days_to_birthday", methods=["GET", "POST"], strict_slashes=False)
def days_to_birthday():
    auth = True if 'login' in session else False
    if not auth:
        return redirect(url_for("index"))

    if request.method == "POST":
        record_id = request.form.get("record_id")
        user_id = session["login"]["id"]

        result = records.how_many_days_to_birthday(record_id, user_id)
        flash(result)

    return render_template("pages/days_to_birthday.html", auth=auth, users2=session["login"]["login"])
