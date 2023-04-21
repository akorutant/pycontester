from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddContestForm(FlaskForm):
    contest_title = StringField("Введите название конкурса", validators=[DataRequired()])
    contest_description = TextAreaField("Введите описание конкурса", validators=[DataRequired()])
    submit = SubmitField("Добавить")