from wtforms import Form, StringField, validators, FieldList, FormField, TextField
from wtforms.validators import ValidationError
from app.utils.util import Util

util = Util()

class StorePdvRequest(Form):
    trading_name = StringField('trading name', [
        validators.DataRequired(),

    ])

    owner_name = StringField('owner name', [
        validators.DataRequired(),
    ])

    document = StringField('document', [
        validators.DataRequired(),
    ])
    def validate_document(self, field):
        if not util.document_is_unique(field.data) or not util.document_is_valid(field.data):
            raise ValidationError("This field is invalid or duplicated")

    address = StringField('address', [
        validators.DataRequired(),
    ])
    def validate_address(form, field):
        point = util.convert_point(field.data)
        if not point.is_valid:
            raise ValidationError("This field is invalid or not exists")

    coverage_area = FieldList(StringField('coverage area', []))
    def validate_coverage_area(self, field):
        multi_polygon = util.convert_multi_polygon(self.coverage_area)
        if len(self.coverage_area) == 0:
            raise ValidationError("This field is required")

        if not multi_polygon.is_valid:
            raise ValidationError("This field is invalid")

    def set_coverage_area(self, coverage_area):
        self.coverage_area = coverage_area
