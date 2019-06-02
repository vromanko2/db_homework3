from flask import Blueprint, abort, jsonify,request,Response

from data import Cohort
from get_session import get_session
cohorts = Blueprint('cohorts', __name__)
#cohort API
@cohorts.route('')
def list_cohorts():
    session = get_session()
    cohort = session.query(Cohort).all()
    res = [c.asdict() for c in cohort]
    return jsonify(res)

@cohorts.route('/<int:id>')
def get_cohorts(id):
    session = get_session()
    cohort = session.query(Cohort).filter(Cohort.id == id).first()
    if cohort is None:
        abort(404, "There's no such cohort id")
    return jsonify(cohort.asdict())

@cohorts.route('', methods=['POST'])
def create_cohort():
    cohort_j = request.get_json()
    if "id" in cohort_j:
        abort(422)
    session = get_session()
    try:
        cohort = Cohort.from_dict(cohort_j)
        session.add(cohort)
        session.commit()
    except () as error:
        abort(422, error)
    return jsonify(cohort.asdict()), 201


@cohorts.route('', methods=['PUT'])
def update_cohort():
    cohort_j = request.get_json()
    if "id" not in cohort_j:
        abort(422, "There's no such id")
    session = get_session()
    cohort = session.query(Cohort).get(cohort_j["id"])
    if cohort is None:
        abort(404, "There's no cohort with such id")
    try:
        cohort.update(cohort_j)
    except () as error:
        abort(422, error)
    session.commit()
    return jsonify(cohort.asdict()), 200


@cohorts.route('/<int:id>', methods=['DELETE'])
def delete_cohort(id):
    session = get_session()
    cohort = session.query(Cohort).get(id)
    if cohort is None:
        abort(404, "There's no such cohort id")
    session.delete(cohort)
    session.commit()
    return Response('', status=200, mimetype='application/json')
