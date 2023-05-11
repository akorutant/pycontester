from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired


class AddContestForm(FlaskForm):
    contest_title = StringField("Введите название конкурса", validators=[DataRequired()])
    contest_description = TextAreaField("Введите описание конкурса", validators=[DataRequired()])
    join_deadline = DateTimeField("Дедлайн начала контеста", validators=[DataRequired()])
    submit = SubmitField("Добавить")