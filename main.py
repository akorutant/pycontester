from flask import Flask, render_template, make_response, request, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.users import User
from data.teachers import Teacher
from data.contests import Contest
from data.tasks import Task
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.change_password_form import ChangePasswordForm
from forms.change_avatar_form import ChangeAvatarForm
from forms.feedback_form import FeedbackForm
from forms.add_contest_form import AddContestForm
from forms.add_tasks_for_contest_form import AddTasksForContestForm

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
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
        return redirect(url_for('login'))

    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("index"))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/account/<int:user_id>", methods=['GET', 'POST'])
@login_required
def account(user_id):
    if current_user.id == user_id:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        form_change_password = ChangePasswordForm()
        form_change_avatar = ChangeAvatarForm()
        if form_change_avatar.validate_on_submit():
            message_for_avatar_form = "Вы не прикрепили файл"
            user_photo = request.files['avatar']
            if user_photo:
                user.avatar = user_photo.read()
                db_sess.commit()
                message_for_avatar_form = "Аватар обновлен"

            return render_template('personal_area.html',
                                   title="Аккаунт",
                                   message_for_avatar_form=message_for_avatar_form,
                                   form_change_password=form_change_password,
                                   form_change_avatar=form_change_avatar)

        elif form_change_password.validate_on_submit():
            message_for_password_form = "Неправильный пароль"
            if user and user.check_password(form_change_password.old_password.data):
                if form_change_password.new_password.data == form_change_password.repeated_new_password.data:
                    user.set_password(form_change_password.repeated_new_password.data)
                    db_sess.commit()
                    message_for_password_form = "Пароль изменён"
                else:
                    message_for_password_form = "Пароли не совпадают"

            return render_template('personal_area.html',
                                   title="Аккаунт",
                                   message_for_password_form=message_for_password_form,
                                   form_change_password=form_change_password,
                                   form_change_avatar=form_change_avatar)

        return render_template('personal_area.html',
                               title="Аккаунт",
                               form_change_password=form_change_password,
                               form_change_avatar=form_change_avatar)

    return redirect(url_for("register"))


@app.route("/code")
@login_required
def code():
    return render_template('code.html')


@app.route("/contests")
@login_required
def contests():
    db_sess = db_session.create_session()
    contests_list = db_sess.query(Contest).all()
    return render_template('contests.html', contests=contests_list)


@app.route("/help")
def help():
    form = FeedbackForm()
    if form.validate_on_submit():
        return render_template('feedback.html', form=form)
    return render_template('feedback.html', form=form)


@app.route("/contests/<int:contest_id>")
@login_required
def contest_code(contest_id):
    db_sess = db_session.create_session()
    contest = db_sess.query(Contest).filter(Contest.id == contest_id).first()
    return render_template('contest_code.html', contest=contest)


@app.route("/contests/teacher_list")
@login_required
def contests_teacher():
    if current_user.job_title == "teacher":
        db_sess = db_session.create_session()
        contests_data = db_sess.query(Contest).filter(Contest.author_id == current_user.id).all()
        return render_template("teacher_contests.html", contests=contests_data)
    return redirect(url_for("index"))


@app.route("/contests/teacher_list/<int:id>", methods=['GET', 'POST'])
@login_required
def contests_edit(id):
    form = AddContestForm()
    if request.form == "GET":
        db_sess = db_session.create_session()
        contests_data = db_sess.query(Contest).filter(Contest.id == id,
                                                      Contest.author_id == current_user.id).first()
        if contests_data:
            form.contest_title.data = contests_data.title
            form.contest_description.data = contests_data.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        contests_data = db_sess.query(Contest).filter(Contest.id == id,
                                                      Contest.author_id == current_user.id).first()
        if contests_data:
            contests_data.title = form.contest_title.data
            contests_data.description = form.contest_description.data
            db_sess.commit()
            return redirect(url_for("contests_teacher"))
        else:
            abort(404)

    return render_template("contests_add.html", form=form)


@app.route("/contests/add", methods=["GET", "POST"])
@login_required
def contests_add():
    if current_user.job_title == "teacher":
        db_sess = db_session.create_session()
        form = AddContestForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            contest = Contest(
                title=form.contest_title.data,
                description=form.contest_description.data,
                author_id=current_user.id
            )
            db_sess.add(contest)
            db_sess.commit()
            return redirect(url_for("contests_teacher"))

        return render_template("contests_add.html", form=form)
    return redirect(url_for("index"))


@app.route("/contest_delete/<int:id>", methods=["GET", "POST"])
@login_required
def contest_delete(id):
    db_sess = db_session.create_session()
    contests_data = db_sess.query(Contest).filter(Contest.id == id,
                                                  Contest.author_id == current_user.id).first()
    if contests_data:
        db_sess.delete(contests_data)
        db_sess.commit()
    else:
        abort(404)
    return redirect(url_for("contests_teacher"))


@app.route("/tasks/<int:contest_id>")
@login_required
def tasks(contest_id):
    db_sess = db_session.create_session()
    tasks_data = db_sess.query(Task).filter(Task.author_id == current_user.id).all()
    if not tasks_data:
        return redirect(url_for("tasks_add", contest_id=contest_id))
    return render_template("tasks.html", tasks=tasks_data)


@app.route("/tasks/add/<int:contest_id>", methods=["GET", "POST"])
@login_required
def tasks_add(contest_id):
    form = AddTasksForContestForm()
    if current_user.job_title == "teacher":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            task = Task(
                title=form.task_title.data,
                description=form.task_description.data,
                input=":".join(form.task_input.data.split()),
                output=":".join(form.task_output.data.split())
            )
        return render_template("add_task_form.html", form=form)


@app.route("/results")
def results():
    return render_template("results.html", title="Результаты")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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
