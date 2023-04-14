from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Никнейм', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    firstname = StringField('Ваше имя', validators=[DataRequired()])
    patronymic = StringField('Ваше отчество', validators=[DataRequired()])
    job_title = RadioField('Кто вы?', choices=[('teacher', 'Учитель'), ('student', 'Ученик')],
                           validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    submit = SubmitField('Зарегестрироваться')
