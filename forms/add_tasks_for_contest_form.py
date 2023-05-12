from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AddTasksForContestForm(FlaskForm):
    task_title = StringField("Введите название задания", validators=[DataRequired()])
    task_description = TextAreaField("Введите условие задания", validators=[DataRequired()])
    task_input = FileField("Введите входные данные (Разделяйте их с помощью #)",
                               validators=[DataRequired()])
    task_output = FileField("Введите выходные данные (Разделяйте их с помощью #)",
                            validators=[DataRequired()])
    submit = SubmitField("Добавить")