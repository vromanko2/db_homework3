from flask import Blueprint, abort, jsonify,request,Response

from data import Transport_Type
from get_session import get_session
transport_types = Blueprint('transport_types', __name__)
@transport_types.route('/')
def list_transport_types():
    session = get_session()
    transport = session.query(Transport_Type).all()
    result = [p.asdict() for p in transport]
    return jsonify(result)


@transport_types.route('/<int:id>')
def get_transport_types(id):
    session = get_session()
    transport = session.query(Transport_Type).filter(Transport_Type.id == id).first()
    if transport is None :
        abort(404, "There's no such transport id")
    return jsonify(transport.asdict())

@transport_types.route('/', methods=['POST'])
def create_transport_type():
    transport_j = request.get_json()
    if "id" in transport_j:
        abort(422)
    session = get_session()
    try:
        transport = Transport_Type.from_dict(transport_j)
        session.add(transport)
        session.commit()
    except () as err:
        abort(422, err)
    return jsonify(transport.asdict()), 201


@transport_types.route('', methods=['PUT'])
def update_transport_type():
    transport_j = request.get_json()
    if "id" not in transport_j:
        abort(422, "There's no such id")
    session = get_session()
    transport = session.query(Transport_Type).get(transport_j["id"])
    if transport is None:
        abort(404, "Transport_type's id is wrong")
    try:
        transport.update(transport_j)
    except () as err:
        abort(422, err)
    session.commit()
    return jsonify(transport.asdict()), 200


@transport_types.route('/<int:id>', methods=['DELETE'])
def delete_transport_type(id):
    session = get_session()
    transport = session.query(Transport_Type).get(id)
    if transport is None:
        abort(404, "Transport's id is wrong")
    session.delete(transport)
    session.commit()
    return Response('', status=200, mimetype='application/json')
