from wtforms import Form, StringField, validators, FieldList, FormField, TextField
from wtforms.validators import ValidationError
from app.utils.document_util import DocumentUtil
from app.utils.point_util import PointUtil
from app.utils.multi_polygon_util import MultiPolygonUtil

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
        document_util = DocumentUtil()
        if (not document_util.document_is_unique(field.data) or
                not document_util.document_is_valid(field.data)):
            raise ValidationError("This field is invalid or duplicated")

    address = StringField('address', [
        validators.DataRequired(),
    ])
    def validate_address(form, field):
        point_util = PointUtil()
        point = point_util.convert_point(field.data)
        if not point.is_valid:
            raise ValidationError("This field is invalid or not exists")

    coverage_area = FieldList(StringField('coverage area', []))
    def validate_coverage_area(self, field):
        multi_polygon_util = MultiPolygonUtil()
        multi_polygon = multi_polygon_util.convert_multi_polygon(
            self.coverage_area)
        if len(self.coverage_area) == 0:
            raise ValidationError("This field is required")

        if not multi_polygon.is_valid:
            raise ValidationError("This field is invalid")

    def set_coverage_area(self, coverage_area):
        self.coverage_area = coverage_area
