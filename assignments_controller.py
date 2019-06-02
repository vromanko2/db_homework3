from flask import Blueprint, abort, jsonify,request,Response

from data import Assignment
from get_session import get_session
assignments = Blueprint('assignments', __name__)

@assignments.route('')
def list_assignments():
    session = get_session()
    assignments = session.query(Assignment).all()
    # import pdb; pdb.set_trace()
    result = [a.asdict() for a in assignments]
    return jsonify(result)

@assignments.route('/<int:id>')
def get_assignment(id):
    session = get_session()
    assignment = session.query(Assignment).filter(Assignment.id == id).first()
    if assignment is None:
        abort(404, "Wrong assignment id!")
    return jsonify(assignment.asdict())

@assignments.route('', methods=['POST'])
def create_assignment():
    assignment_json = request.get_json()
    if "id" in assignment_json:
        abort(422)
    session = get_session()
    try:
        assignment = Assignment.from_dict(assignment_json)
    except () as err:
        abort(422, err)
    # import pdb; pdb.set_trace()
    session.add(assignment)
    session.commit()
    return jsonify(assignment.asdict()), 201


@assignments.route('', methods=['PUT'])
def update_assignment():
    assignment_json = request.get_json()
    if "id" not in assignment_json:
        abort(422, "There's no such id")
    session = get_session()
    assignment_existing = session.query(Assignment).get(assignment_json['id'])
    # import pdb; pdb.set_trace()
    if assignment_existing is None:
        abort(404, "There's no such assignment id")
    try:
        assignment_existing.update(assignment_json)
    except () as err:
        abort(422, err)
    session.commit()
    return jsonify(assignment_existing.asdict()), 200


@assignments.route('/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    session = get_session()
    assignment_existing = session.query(Assignment).get(id)
    if assignment_existing is None:
        abort(404, "There's no such id")
    session.delete(assignment_existing)
    session.commit()
    return Response('', status=200, mimetype='application/json')

