from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, TelField
from wtforms.validators import DataRequired, Length, Email

class FormsLogin(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6 ,50)])
    submit = SubmitField("Login")


class FormsCadastro(FlaskForm):
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(),Length(6, 100)])
    telefone = TelField("Telefone", validators=[DataRequired(), Length(11)])
    submit = SubmitField("Fazer cadastro")

