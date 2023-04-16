from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Старый пароль"})
    new_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Новый пароль"})
    repeated_new_password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Повторите новый пароль"})
    submit = SubmitField("Сменить")