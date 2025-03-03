from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FormsLocation(FlaskForm):
    latitude = FloatField(
        "Latitude",
        default=0.0000,
        validators=[DataRequired(), NumberRange(-90.0000, 90.0000)],
        render_kw={"step": "0.00001"}  # Limita a 5 casas decimais
    )

    longitude = FloatField(
        "Longitude",
        default=0.0000,
        validators=[DataRequired(), NumberRange(-180.0000, 180.0000)],
        render_kw={"step": "0.0001"}  # Limita a 5 casas decimais
    )

    submit = SubmitField("Enviar")