import phonenumbers
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField,FloatField,TextAreaField,BooleanField,DateField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError

class LoginForm(FlaskForm):
    username=StringField(label='Username: ', validators=[DataRequired()]) 
    password=PasswordField(label='Password: ',validators=[DataRequired()])
    submit=SubmitField(label='Login')
    recaptcha = RecaptchaField()
    
class AddCustomerForm(FlaskForm):
    phone=StringField(label='Enter Phone: ',validators=[DataRequired(),Length(min=10,max=10)])
    name=StringField(label='Enter Name: ',validators=[DataRequired()])
    address=TextAreaField(label='Enter Address: ',validators=[DataRequired()])
    balance=FloatField(label='Enter Balance: ',validators=[DataRequired()])
    submit=SubmitField(label='Add Customer')
    
    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        
class OrderForm(FlaskForm):
    phone = StringField(label='Enter Phone ',validators=[DataRequired(),Length(min=10,max=10)])
    detail = TextAreaField(label='Enter Detail ',validators=[DataRequired()])
    amount = FloatField(label='Enter Amount ',validators=[DataRequired()])
    paid = FloatField(label='Enter Amount Paid ')
    date_added = DateField(label='Enter Date ',validators=[DataRequired()])
    submit = SubmitField(label='Add Order')