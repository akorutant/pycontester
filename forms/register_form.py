from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    login = StringField('Никнейм', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    firstname = StringField('Ваше имя', validators=[DataRequired()])
    patronymic = StringField('Ваше отчество', validators=[DataRequired()])
    job_title = RadioField('Кто вы?', choices=[('teacher', 'Учитель'), ('student', 'Ученик')],
                           validators=[DataRequired()], default='student')
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=32, message='Паполь должен быть не меньше 8 символов, не более 32 символов')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    select = BooleanField("Принять условия пользовательского соглашения", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
