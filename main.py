from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.teachers import Teacher
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "fjkFOEKFMOKMFIO3FMKLMkelfmOIJR3FMFKNFOU2IN3PIFNOI232F"

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("database/db.sqlite")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            firstname=form.firstname.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            job_title=form.job_title.data,
            email=form.email.data
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        if form.job_title.data == "teacher":
            user_id = db_sess.query(User).filter_by(email=form.email.data).first()
            print(user_id)
            teacher = Teacher(
                user_id=user_id
            )
            db_sess.add(teacher)
            db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/account/<int:user_id>")
def account(user_id):
    pass


@app.route("/code")
def code():
    if current_user.is_authenticated:
        return render_template('index2.html')
    else:
        return redirect("/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(debug=True)
