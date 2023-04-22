from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddTasksForContestForm(FlaskForm):
    task_title = StringField("Введите название задания", validators=[DataRequired()])
    task_description = TextAreaField("Введите условие задания", validators=[DataRequired()])
    task_input = TextAreaField("Введите входные данные", validators=[DataRequired()])
    task_output = TextAreaField("Введите выходные данные", validators=[DataRequired()])
    submit = SubmitField("Добавить")