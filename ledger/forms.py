from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError

class LoginForm(FlaskForm):
    username=StringField(label='Username: ', validators=[DataRequired()]) 
    password=PasswordField(label='Password: ',validators=[DataRequired()])
    submit=SubmitField(label='Login')
    recaptcha = RecaptchaField()