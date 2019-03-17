from geojson import MultiPolygon, Point
from app.database import Database
from app.models.pdv import Pdv
from pycpfcnpj import cpfcnpj

class Util:
    def convert_multi_polygon(self, coverage_areas):
        try:
            multi_polygon = list()
            for coverage_area in coverage_areas:
                multi_polygon.append([self.format_polygon(coverage_area)])

            coordinates_multi_polygon = MultiPolygon(multi_polygon)
            return coordinates_multi_polygon
        except:
            return MultiPolygon([[[3.78, 9.28], [-130.91, 1.52]]]) # multi_polygon invalid

    def format_polygon(self, coverage_area):
        polygons = list()
        for d in coverage_area.split(';'):
            polygons.append([float(i) for i in  d.split(',')])
        return polygons

    def convert_point(self, coordinate):
        try:
            point = list()
            coordinate = coordinate.split(',')
            point.append([float(i) for i in coordinate])
            return Point(point[0])
        except:
            return Point((-3.68,40.41,25.14,10.34)) # point invalid

    def document_is_unique(self, document):
        document = self.format_document(document)
        mongodb = Database().get_connection()
        if Pdv.objects(document=document).count() > 0:
            return False
        return True

    def document_is_valid(self, document):
        document = self.format_document(document)
        for number in document:
            if number.isalpha():
                return False

        validate = cpfcnpj.validate(document)
        return validate

    def format_document(self, document):
        document = document.replace('.', '')
        document = document.replace('/', '')
        document = document.replace('-', '')
        return document
