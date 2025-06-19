from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class FormRegistro(FlaskForm):
    """
    Formulario de registro para nuevos usuarios.

    Define los campos necesarios para que un usuario se registre en el sistema,
    incluyendo validaciones básicas para asegurar la calidad de los datos.

    Campos:
        nombre (StringField): Nombre del usuario. Requerido, longitud entre 2 y 30.
        apellido (StringField): Apellido del usuario. Requerido, longitud entre 2 y 30.
        username (StringField): Nombre de usuario. Requerido, longitud entre 3 y 30.
        claustro (SelectField): Tipo de claustro del usuario ("estudiante", "docente", "pays"). Requerido.
        email (StringField): Correo electrónico. Requerido, formato de email válido.
        password (PasswordField): Contraseña. Requerido, al menos 8 caracteres y debe coincidir con la confirmación.
        confirmacion (PasswordField): Repetición de la contraseña para verificación. Requerido.
        submit (SubmitField): Botón para enviar el formulario.
    """
    nombre=StringField(label= "Nombre", validators=[DataRequired(), Length(min=2, max=30)])
    apellido=StringField(label="Apellido", validators=[DataRequired(), Length(min=2, max=30)])
    username=StringField(label="Nombre de usuario", validators=[DataRequired(), Length(min=3, max=30)])
    claustro=SelectField("Claustro", choices=[("estudiante","Estudiante"),
                                              ("docente","Docente"),
                                              ("pays","PAyS")])
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password= PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=8, message= "La contraseña debe tener al menos 8 caracteres."),
        EqualTo('confirmacion', message='Las contraseñas deben ser iguales')
        ])
    confirmacion= PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit= SubmitField(label='Registrar')

class FormLogin(FlaskForm):
    """
    Formulario de inicio de sesión.

    Define los campos para que un usuario pueda autenticarse en el sistema.

    Campos:
        email (StringField): Correo electrónico del usuario. Requerido, formato de email válido.
        password (PasswordField): Contraseña del usuario. Requerido, al menos 4 caracteres.
        submit (SubmitField): Botón para enviar el formulario.
    """
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField(label='Ingresar')

class FormReclamo(FlaskForm):
    """
    Formulario para la creación de un nuevo reclamo.

    Permite a los usuarios ingresar la descripción del problema, seleccionar
    un departamento y, opcionalmente, adjuntar una imagen.

    Campos:
        descripcion (TextAreaField): Descripción detallada del problema.
                                     Requerido, longitud entre 10 y 1000 caracteres.
        departamento (SelectField): Campo de selección para el departamento al que se asigna el reclamo.
                                    Las opciones se cargan dinámicamente en la ruta de Flask. Requerido.
        foto (FileField): Campo para adjuntar una imagen (opcional).
                          Solo se permiten archivos JPG, PNG y JPEG.
        submit (SubmitField): Botón para enviar el reclamo.
    """
    descripcion= TextAreaField("Descripción", validators=[DataRequired(), Length(min=10, max=1000)])
    departamento= SelectField("Departamento", choices=[], validators=[DataRequired()])
    foto= FileField("Adjuntar Imagen (opcional)", validators=[FileAllowed(['jpg','png','jpeg'], "Solo imágenes")])
    submit=SubmitField("Enviar Reclamo")
    