from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, AnyOf

# Formulario para el login
class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[InputRequired()])
    password = PasswordField('Contraseña:', validators=[InputRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Login')