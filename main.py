import os
import datetime as dt
from io import BytesIO

from flask import Flask, render_template, make_response, request, abort, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from data import db_session
from data.contests import Contest
from data.tasks import Task
from data.teachers import Teacher
from data.users import User
from forms.add_contest_form import AddContestForm
from forms.add_tasks_for_contest_form import AddTasksForContestForm
from forms.change_avatar_form import ChangeAvatarForm
from forms.change_password_form import ChangePasswordForm
from forms.feedback_form import FeedbackForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.add_task_to_contest import AddTasksToContestForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "fjkFOEKFMOKMFIO3FMKLMkelfmOIJR3FMFKNFOU2IN3PIFNOI232F"

login_manager = LoginManager()
login_manager.init_app(app)

if not os.path.isdir('database'):
    os.mkdir('database')

if not os.path.isfile('database/db.sqlite'):
    with open('database/db.sqlite', 'w') as f:
        pass

db_session.global_init("database/db.sqlite")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/main')
def index():
    return render_template('index.html',
                           title="Главная")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
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
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


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
                               title='Авторизация',
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


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
    return render_template('code.html',
                           title="Редактор кода")


#

@app.route("/contests")
@login_required
def contests():
    db_sess = db_session.create_session()
    contests_list = db_sess.query(Contest).all()
    return render_template('contests.html',
                           title="Список конкурсов",
                           contests=contests_list)


@app.route("/help")
def help():
    form = FeedbackForm()
    if form.validate_on_submit():
        return render_template('feedback.html',
                               title="Обратная связь",
                               form=form)
    return render_template('feedback.html',
                           title="Обратная связь",
                           form=form)


@app.route("/contests/<int:contest_id>", methods=['GET', 'POST'])
@login_required
def contests_list(contest_id):
    db_sess = db_session.create_session()
    contest = db_sess.query(Contest).filter(Contest.id == contest_id).first()
    task_data = contest.tasks
    return render_template('contest_code.html',
                           title="Редактор кода",
                           contest=contest,
                           tasks=task_data
                           )


@app.route("/contests/teacher_list")
@login_required
def contests_teacher():
    if current_user.job_title == "teacher":
        db_sess = db_session.create_session()
        contests_data = db_sess.query(Contest).filter(Contest.author_id == current_user.id).all()
        return render_template("teacher_contests.html",
                               title="Список конкурсов",
                               contests=contests_data)
    return redirect(url_for("index"))


@app.route("/contests/teacher_list/<int:id>", methods=['GET', 'POST'])
@login_required
def contests_edit(id):
    form = AddContestForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        contests_data = db_sess.query(Contest).filter(Contest.id == id,
                                                      Contest.author_id == current_user.id).first()
        if contests_data:
            form.contest_title.data = contests_data.title
            form.contest_description.data = contests_data.description
            form.submit.data = "Обновить"
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
    return render_template("contests_add.html",
                           title="Редакторование конкурcов",
                           form=form,
                           current_datetime=dt.datetime.now())


@app.route("/contests/add", methods=["GET", "POST"])
@login_required
def contests_add():
    if current_user.job_title == "teacher":
        form = AddContestForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            # deadline = dt.datetime.strptime(form.join_deadline.data, '%Y-%m-%dT%H:%M')
            contest = Contest(
                title=form.contest_title.data,
                description=form.contest_description.data,
                author_id=current_user.id,
                deadline=form.join_deadline.data
            )
            db_sess.add(contest)
            db_sess.commit()
            return redirect(url_for("contests_teacher"))
        return render_template("contests_add.html",
                               title="Добавление конкурcов",
                               form=form,
                               current_datetime=dt.datetime.now())
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


@app.route("/tasks/<int:contest_id>", methods=['GET', 'POST'])
@login_required
def tasks(contest_id):
    form = AddTasksToContestForm()
    db_sess = db_session.create_session()
    tasks_data = db_sess.query(Task).filter(Task.author_id == current_user.id).all()
    contest_data = db_sess.query(Contest).filter(Contest.id == contest_id).first()
    if form.validate_on_submit():
        task_id = request.form.get('id')
        task = db_sess.query(Task).filter(Task.id == task_id).first()
        contest_data.tasks.append(task)
        db_sess.commit()
    if not tasks_data:
        return redirect(url_for("tasks_add",
                                contest_id=contest_id))
    return render_template("tasks.html",
                           title="Список конкурсов",
                           tasks=tasks_data,
                           contest=contest_data,
                           form=form)


@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def tasks_add():
    form = AddTasksForContestForm()
    if current_user.job_title == "teacher":
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            input_file = form.task_input.data
            output_file = form.task_output.data
            input_file = str(input_file.read())[2:-1].replace(r"\r\n", "!!!")
            output_file = str(output_file.read())[2:-1].replace(r"\r\n", "!!!")

            task = Task(
                title=form.task_title.data,
                description=form.task_description.data,
                input=input_file,
                output=output_file,
                author_id=current_user.id
            )
            db_sess.add(task)
            db_sess.commit()
            flash('Задание создано!')
            return render_template("add_task_form.html",
                                   title="Добавление задачи",
                                   form=form)
        return render_template("add_task_form.html",
                               title="Добавление задачи",
                               form=form)
    return abort(404)


@app.route("/task_delete/<int:contest_id>/<int:id>")
def task_delete(contest_id, id):
    db_sess = db_session.create_session()
    task_data = db_sess.query(Task).filter(Task.id == id).first()
    if task_data:
        contest = db_sess.query(Contest).filter(Contest.id == contest_id).first()
        contest.tasks.remove(task_data)
        db_sess.commit()
    else:
        abort(404)
    return redirect(url_for("tasks", contest_id=contest_id))


@app.route("/tasks/<int:contest_id>/<int:id>", methods=['GET', 'POST'])
@login_required
def task_edit(contest_id, id):
    form = AddTasksForContestForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        task_data = db_sess.query(Task).filter(Task.id == id,
                                               Task.author_id == current_user.id).first()
        if task_data:
            form.task_title.data = task_data.title
            form.task_description.data = task_data.description
            form.task_input.data = task_data.input
            form.task_output.data = task_data.output
            form.submit.data = "Обновить"
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task_data = db_sess.query(Task).filter(Contest.id == id,
                                               Task.author_id == current_user.id).first()
        if task_data:
            task_data.title = form.task_title.data
            task_data.description = form.task_description.data
            task_data.input = form.task_input.data
            task_data.output = form.task_output.data
            db_sess.commit()
            return redirect(url_for("tasks",
                                    contest_id=contest_id))
        else:
            abort(404)

    return render_template("add_task_form.html",
                           title="Редактор задачи",
                           form=form)


@app.route("/results")
def results():
    return render_template("results.html",
                           title="Результаты")


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
        with open('static/img/avatar.jpeg', 'rb') as image:
            img = image.read()
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.errorhandler(503)
def not_found(error):
    return render_template('503error.html',
                           title="Ошибка 503"), 503


@app.errorhandler(500)
def not_found(error):
    return render_template('500error.html',
                           title="Ошибка 500"), 500


@app.errorhandler(405)
def not_allowed(error):
    return render_template('405error.html',
                           title="Ошибка 405"), 405


@app.errorhandler(404)
def not_found(error):
    return render_template('404error.html',
                           title="Ошибка 404"), 404


@app.errorhandler(403)
def not_found(error):
    return render_template('403error.html',
                           title="Ошибка 403"), 403


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401error.html',
                           title="Ошибка 401"), 401


if __name__ == '__main__':
    app.run(debug=True)
