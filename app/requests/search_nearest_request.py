from wtforms import Form, StringField, validators, FloatField
from wtforms.validators import ValidationError
from app.utils.point_util import PointUtil

class SearchNearestRequest(Form):
    coordinate = StringField('coordinate', [
        validators.DataRequired()
    ])

    def validate_coordinate(form, field):
        point_util = PointUtil()
        coordinate = point_util.convert_point(field.data)
        if not coordinate.is_valid:
            raise ValidationError("This field is invalid")

    max_distance = FloatField('max distance', [
        validators.DataRequired()
    ])
