from wtforms import Form, StringField, validators
from app.models.pdv import Pdv
from app.database import Database
from wtforms.validators import ValidationError
import bson

class GetByIdRequest(Form):
    id = StringField('id', [
        validators.DataRequired(),
    ])
    def validate_id(form, field):
        mongodb = Database().get_connection()
        try:
            Pdv.objects(id=bson.objectid.ObjectId(field.data))[0]
        except:
            raise ValidationError("Pdv not found")
