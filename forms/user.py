from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Никнейм', validators=[DataRequired()])
    firstname = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    patronymic = StringField('Ваше отчество', validators=[DataRequired()])
    job_title = StringField('Ваша должность', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    submit = SubmitField('Зарегестрироваться')
