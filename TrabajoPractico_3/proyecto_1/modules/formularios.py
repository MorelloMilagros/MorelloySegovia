from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class FormRegistro(FlaskForm):
    nombre=StringField(label= "Nombre", validators=[DataRequired(), Length(min=2, max=50)])
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password= PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=8, message= "La contraseña debe tener al menos 8 caracteres."),
        EqualTo('confirmacion', message='Las contraseñas deben ser iguales')
        ])
    confirmacion= PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit= SubmitField(label='Registrar')

class FormLogin(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField(label='Ingresar')

class FormReclamo(FlaskForm):
    descripcion= TextAreaField("Descripción", validators=[DataRequired(), Length(min=10, max=1000)])
    departamento= SelectField("Departamento", choices=[("Atención al cliente", "Atención al cliente"),
                                                       ("Soporte técnico","Soporte Técnico"),
                                                       ("Facturación","Facturación")],
                                                       validators=[DataRequired()])
    submit=SubmitField("Enviar Reclamo")
    