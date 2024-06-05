from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from app.models import User, UserInfo, Client, Center


ma = Marshmallow()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    password = auto_field(load_only=True)
    email = auto_field(data_key='email')  # Field alias

    @validates('email')
    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('Correo electrónico no válido.')


class LoginSchema(ma.Schema):
    """ Serializer for logs users in """
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El campo de correo es requerido.",
            "null": "Este campo de correo no debe estar vacío.",
            "validator_failed": "El correo ingresado no es válido.",
            "invalid": "El valor ingresado no es un correo electrónico válido."
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            "required": "El campo de password es requerido.",
            "null": "Este campo de password no debe estar vacío.",
            "validator_failed": "La password ingresada no es válida.",
            "invalid": "El valor ingresado no es una contraseña válida."
        }
    )


class UserInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserInfo
        include_fk = True


class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client


class CenterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Center
        load_instance = True