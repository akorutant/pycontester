from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    firstname = StringField("Ваше имя", validators=[DataRequired()])
    surname = StringField("Ваша фамилия", validators=[DataRequired()])
    email = EmailField("Ваш email", validators=[DataRequired()])
    user_message = TextAreaField("Сообщение", validators=[DataRequired()])
    submit = SubmitField("Отправить")