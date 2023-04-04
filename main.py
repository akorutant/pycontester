from flask import Flask, render_template
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)


@app.route('/')
def index():
    db_session.global_init("database/database.sqlite")
    return render_template('index.html')


@app.route('/register')
def register():
    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
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
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')

        return render_template('register.html', title='Регистрация', form=form)


@app.route("/login")
def login():
    ...


if __name__ == '__main__':
    app.run(debug=True)
