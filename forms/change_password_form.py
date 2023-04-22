from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Старый пароль"})
    new_password = PasswordField(validators=[DataRequired(), Length(min=8, max=32, message='Паполь должен быть не меньше 8 символов, не более 32 символов')], render_kw={"placeholder": "Новый пароль"})
    repeated_new_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Повторите новый пароль"})
    submit = SubmitField("Сменить")