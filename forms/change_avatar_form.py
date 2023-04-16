from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class ChangeAvatarForm(FlaskForm):
    avatar = FileField(validators=[DataRequired()])
    submit = SubmitField("Сменить")
