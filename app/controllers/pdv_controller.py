from app.models.pdv import Pdv
from app.database import Database
import bson
from app.utils.point_util import PointUtil
from app.utils.multi_polygon_util import MultiPolygonUtil
from app.utils.document_util import DocumentUtil

class PdvController:
    def store(self, **kwargs):
        mongodb = Database().get_connection()
        multi_polygon_util = MultiPolygonUtil()
        document_util = DocumentUtil()
        point_util = PointUtil()

        multi_polygon = multi_polygon_util.convert_multi_polygon(kwargs['coverage_area'])
        point = point_util.convert_point(kwargs['address'])
        document = document_util.format_document(kwargs['document'])

        pdv = Pdv(
            document=document,
            owner_name=kwargs['owner_name'],
            trading_name=kwargs['trading_name'],
            coverage_area=multi_polygon,
            address=point
        ).save()

        return pdv.to_json()

    def get_by_id(self, id):
        mongodb = Database().get_connection()
        pdv =  Pdv.objects(id=bson.objectid.ObjectId(id))[0]
        return pdv.to_json()

    def search_nearest(self, **kwargs):
        mongodb = Database().get_connection()
        point_util = PointUtil()
        coordinate = point_util.convert_point(kwargs['coordinate'])
        pdvs =  Pdv.objects(address__near=coordinate,
            address__max_distance=float(kwargs['max_distance']))

        data = list()
        for pdv in pdvs:
            data.append(pdv.to_json())

        return data
