from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2= PasswordField('Repite tu Contraseña', validators=[DataRequired(),EqualTo('password', 'Las contraseñas no coinciden')])
    submit = SubmitField('Registrarse')