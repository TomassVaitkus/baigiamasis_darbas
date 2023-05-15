from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, InputRequired


class OrderForm(FlaskForm):
    vardas = StringField('Vardas', [DataRequired(message='Lauką būtina užpildyti')])
    pavarde = PasswordField('Pavardė', validators=[Length(min=8, message=('Per mažai simbolių!')), DataRequired(message='Lauką būtina užpildyti')])
    address1 = StringField('Adresas (pirma eilutė)', validators=[DataRequired(message=('Lauką būtina užpildyti')), Length(min=4, message=('Per mažai simbolių!'))])
    address2 = StringField('Adresas (antra eilutė)', validators=[Length(min=4, message=('Per mažai simbolių'))])
    city = StringField('Miestas', validators=[DataRequired(message='Lauką būtina užpildyti'), Length(min=4, message=('Per mažai simbolių'))])
    zip_code = StringField('Pašto kodas', validators=[DataRequired(message='Lauką būtina užpildyti'), Length(min=4, message=('Per mažai simbolių'))])
    agree = BooleanField('Patvirtinu, kad užsakymas teisingas') 
    telnr = StringField('Telefono Nr.', validators=[DataRequired(message='Lauką būtina užpildyti'), Length(min=9, message=('Per mažai simbolių'))])
    pastabos = StringField('Pastabos')
    email =  StringField('Elektroninis paštas', validators=[DataRequired(message='Lauką būtina užpildyti')])
    submit = SubmitField('Submit')