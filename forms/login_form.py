from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=32, message='Паполь должен быть не меньше 8 символов, не более 32 символов')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
