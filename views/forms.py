from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.fields import EmailField


class LoginPasswordForm(FlaskForm):
    login = EmailField('E-mail', validators=[DataRequired(), Email('Введите корректный адрес электронной почты')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')


class LoginTokenForm(FlaskForm):
    token = PasswordField('Токен', validators=[DataRequired()], render_kw={'autofocus': True})
    remember = BooleanField('Запомнить меня')
