from flask import Flask, request, jsonify
from app.requests.store_pdv_request import StorePdvRequest
from app.requests.get_by_id_request import GetByIdRequest
from app.requests.search_nearest_request import SearchNearestRequest
from app.utils.util import Util
from app.models.pdv import Pdv
from app.database import Database
import bson
import simplejson

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create():
    inputs = StorePdvRequest(request.form)
    inputs.set_coverage_area(request.form.getlist('coverage_area[]'))
    util = Util()
    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    multi_polygon = util.convert_multi_polygon(request.form.getlist('coverage_area[]'))
    document = request.form.get('document')
    point = util.convert_point(request.form.get('address'))

    pdv = Pdv(
        document=util.format_document(document),
        owner_name=request.form.get('owner_name'),
        trading_name=request.form.get('trading_name'),
        coverage_area=multi_polygon,
        address=point
    )
    pdv = pdv.save()
    return jsonify(success=True, data=pdv.to_json())

@app.route('/get-by-id', methods=['GET'])
def get_by_id():
    mongodb = Database().get_connection()
    inputs = GetByIdRequest(request.args)

    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    pdv =  Pdv.objects(id=bson.objectid.ObjectId(request.args.get('id')))[0]
    return jsonify(success=True, data=pdv.to_json())

@app.route('/search-nearest', methods=['GET'])
def search_nearest():
    mongodb = Database().get_connection()
    inputs = SearchNearestRequest(request.args)
    util = Util()
    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    coordinate = util.convert_point(request.args.get('coordinate'))
    pdvs =  Pdv.objects(address__near=coordinate,
        address__max_distance=float(request.args.get('max_distance')))
    data = list()
    for pdv in pdvs:
        data.append(pdv.to_json())

    return jsonify(success=True, data=data)

if (__name__ == "__main__"):
    app.run(port=5000)
