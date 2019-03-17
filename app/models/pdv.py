import mongoengine
import bson

class Pdv(mongoengine.Document):
    trading_name = mongoengine.StringField(required=True)
    owner_name = mongoengine.StringField(required=True)
    document = mongoengine.StringField(required=True, unique=True)
    coverage_area = mongoengine.fields.MultiPolygonField(auto_index=True, required=True)
    address = mongoengine.fields.PointField(auto_index=True, required=True)

    def to_json(self):
        pdv = self.to_mongo()
        pdv['_id'] = str(pdv['_id'])
        data = bson.json_util.dumps(pdv)
        data = bson.json_util.loads(data)
        return data
