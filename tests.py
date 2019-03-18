from app.requests.get_by_id_request import GetByIdRequest
from mongoengine import connect, errors
from app.models.pdv import Pdv
from app.config import Config
from wtforms.validators import ValidationError
from app.utils.document_util import DocumentUtil
from app.utils.point_util import PointUtil
from app.utils.multi_polygon_util import MultiPolygonUtil

document_util = DocumentUtil()
point_util = PointUtil()
multi_polygon_util = MultiPolygonUtil()
config = Config()
config = config.get_config()

def test_convert_multi_polygon_valid():
    multi_polygon = list()
    multi_polygon.append('30,20;45,40;10,40;30,20')
    multi_polygon.append('15,5;40,10;10,20;5,10;15,5')
    multi_polygon = multi_polygon_util.convert_multi_polygon(multi_polygon)
    assert multi_polygon.is_valid == True

def test_convert_multi_polygon_invalid():
    multi_polygon = list()
    multi_polygon.append('30,20;345,401231230,2120')
    multi_polygon.append('15as,540qw,123;10,20231;5,10;15,1235')
    multi_polygon.append('test')
    multi_polygon = multi_polygon_util.convert_multi_polygon(multi_polygon)
    assert multi_polygon.is_valid == False

def test_convert_point_valid():
    point = '100.0,0.0'
    point = point_util.convert_point(point)
    assert point.is_valid == True

def test_convert_point_invalid():
    point = 'test,123,0391,point'
    point = point_util.convert_point(point)
    assert point.is_valid == False

def test_document_is_valid():
    document = '60.738.043/0001-09'
    document = document_util.document_is_valid(document)
    assert document == True

def test_document_is_not_valid():
    document = '60test738asd0431165/000asd2309'
    document = document_util.document_is_valid(document)
    assert document == False

def test_format_document():
    document = '60.738.043/0001-09'
    document = document_util.format_document(document)
    assert document == '60738043000109'

def test_create_pdv():
    connection = connect(config['mongodb_mock']['db'],
        host='mongomock://' + config['mongodb_mock']['host'])

    multi_polygon = list()
    multi_polygon.append('30,20;45,40;10,40;30,20')
    multi_polygon.append('15,5;40,10;10,20;5,10;15,5')
    multi_polygon = multi_polygon_util.convert_multi_polygon(multi_polygon)

    point = '10.0,20.0'
    point = point_util.convert_point(point)

    pdv = Pdv(
        document=document_util.format_document('60.738.043/0001-09'),
        owner_name='test',
        trading_name='test',
        coverage_area=multi_polygon,
        address=point
    )
    pdv = pdv.save()
    pdv = Pdv.objects().count()
    connection.drop_database(config['mongodb_mock']['db'])
    assert pdv > 0

def test_document_unique():
    connection = connect(config['mongodb_mock']['db'],
        host='mongomock://' + config['mongodb_mock']['host'])

    multi_polygon = list()
    multi_polygon.append('30,20;45,40;10,40;30,20')
    multi_polygon.append('15,5;40,10;10,20;5,10;15,5')
    multi_polygon = multi_polygon_util.convert_multi_polygon(multi_polygon)

    point = '10.0,20.0'
    point = point_util.convert_point(point)

    pdv = Pdv(
        document=document_util.format_document('60.738.043/0001-09'),
        owner_name='test',
        trading_name='test',
        coverage_area=multi_polygon,
        address=point
    )
    pdv = pdv.save()

    pdv_unique = Pdv(
        document=document_util.format_document('60.738.043/0001-09'),
        owner_name='test',
        trading_name='test',
        coverage_area=multi_polygon,
        address=point
    )
    try:
        pdv_unique = pdv_unique.save()
    except errors.NotUniqueError:
        connection.drop_database(config['mongodb_mock']['db'])
        assert False == False
