from flask import Flask, request, jsonify
from app.requests.store_pdv_request import StorePdvRequest
from app.requests.get_by_id_request import GetByIdRequest
from app.requests.search_nearest_request import SearchNearestRequest
from app.controllers.pdv_controller import PdvController

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create():
    inputs = StorePdvRequest(request.form)
    inputs.set_coverage_area(request.form.getlist('coverage_area[]'))
    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    pdv = PdvController()
    pdv = pdv.store(
        document=request.form.get('document'),
        owner_name=request.form.get('owner_name'),
        trading_name=request.form.get('trading_name'),
        coverage_area=request.form.getlist('coverage_area[]'),
        address=request.form.get('address')
    )

    return jsonify(success=True, data=pdv)

@app.route('/get-by-id', methods=['GET'])
def get_by_id():
    inputs = GetByIdRequest(request.args)

    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    pdv = PdvController()
    pdv = pdv.get_by_id(request.args.get('id'))

    return jsonify(success=True, data=pdv)

@app.route('/search-nearest', methods=['GET'])
def search_nearest():
    inputs = SearchNearestRequest(request.args)
    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    pdv = PdvController()
    pdvs = pdv.search_nearest(
        coordinate=request.args.get('coordinate'),
        max_distance=request.args.get('max_distance'))

    return jsonify(success=True, data=pdvs)

if (__name__ == "__main__"):
    app.run(port=5000)
