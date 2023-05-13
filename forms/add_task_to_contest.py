from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AddTasksToContestForm(FlaskForm):
    id = StringField()
    submit = SubmitField("Добавить")
