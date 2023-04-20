from flask import Flask, render_template, make_response, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.users import User
from data.teachers import Teacher
from data.contests import Contest
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.change_password_form import ChangePasswordForm
from forms.change_avatar_form import ChangeAvatarForm
from forms.feedback_form import FeedbackForm

from rate_function import APICurrencyRates

app = Flask(__name__)
currency_rates = APICurrencyRates("M3ZLsRpZnrb80mAb6ZobImQWTo8oe2qg", "RUB", "USD", 1)
app.config["SECRET_KEY"] = "fjkFOEKFMOKMFIO3FMKLMkelfmOIJR3FMFKNFOU2IN3PIFNOI232F"

login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("database/db.sqlite")


# TODO когда будем заливать на хост, то нужно в каждом роуте прописать rate=currency_rates.get_current_rate()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/main')
def index():
    return render_template('index.html', title="Главная",
                           rate="81")  # rate=currency_rates.get_current_rate() убрал т.к у апи ограничение


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
            user = db_sess.query(User).filter_by(email=form.email.data).first()
            teacher = Teacher(
                user_id=user.id
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


@app.route("/account/<int:user_id>", methods=['GET', 'POST'])
def account(user_id):
    if current_user.id == user_id:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        form_change_password = ChangePasswordForm()
        form_change_avatar = ChangeAvatarForm()
        if form_change_avatar.validate_on_submit():
            user_photo = request.files['avatar']
            if user_photo:
                user.avatar = user_photo.read()
                db_sess.commit()
                return render_template('personal_area.html',
                                       message_for_avatar_form="Аватар обновлен",
                                       form_change_password=form_change_password,
                                       form_change_avatar=form_change_avatar)
            return render_template('personal_area.html',
                                   message_for_avatar_form="Вы не прикрепили файл",
                                   form_change_password=form_change_password,
                                   form_change_avatar=form_change_avatar)

        elif form_change_password.validate_on_submit():
            if user and user.check_password(form_change_password.old_password.data):
                if form_change_password.new_password.data == form_change_password.repeated_new_password.data:
                    user.set_password(form_change_password.repeated_new_password.data)
                    db_sess.commit()
                    return render_template('personal_area.html',
                                           message_for_password_form="Пароль изменен",
                                           form_change_password=form_change_password,
                                           form_change_avatar=form_change_avatar)

                return render_template('personal_area.html',
                                       message_for_password_form="Пароли не совпадают",
                                       form_change_password=form_change_password,
                                       form_change_avatar=form_change_avatar)

            return render_template('personal_area.html',
                                   message_for_password_form="Неправильный пароль",
                                   form_change_password=form_change_password,
                                   form_change_avatar=form_change_avatar)

        return render_template('personal_area.html',
                               title="Аккаунт",
                               form_change_password=form_change_password,
                               form_change_avatar=form_change_avatar)

    return redirect("/register")


@app.route("/code")
def code():
    if current_user.is_authenticated:
        return render_template('code.html')
    return redirect("/register")


@app.route("/contests")
def contests():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        contests_list = db_sess.query(Contest).all()
        return render_template('contests.html', contests=contests_list)
    return redirect("/register")


@app.route("/help")
def help():
    form = FeedbackForm()
    if form.validate_on_submit():
        return render_template('feedback.html', form=form)
    return render_template('feedback.html', form=form)


@app.route("/contests/<int:contest_id>")
def contest_code(contest_id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        contest1 = db_sess.query(Contest).filter(Contest.id == contest_id).first()
        return render_template('contest_code.html', contest=contest1)
    return redirect("/register")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/user_avatar")
@login_required
def user_avatar():
    img = current_user.avatar
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(debug=True, port=8080)
