from flask import Flask, render_template, request, redirect, url_for
from task_03.model import db, User
from task_03.forms import RegisterForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)
app.config["SECRET_KEY"] = "mysecretkey"
csrf = CSRFProtect(app)


@app.route("/")
def index():
    return "Hello"


@app.cli.command("init_db")
def init_db():
    db.create_all()
    print("DB create!")


@app.route("/registration/", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        user = User(
            name=name,
            surname=surname,
            email=email,
            password=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("success"))
    else:
        return render_template("registration.html", form=form)


@app.route("/success/")
def success():
    return render_template("success.html")
