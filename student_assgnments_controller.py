from flask import Blueprint, abort, jsonify, request,Response

from data import Student_Assignment
from get_session import get_session

students_assignments = Blueprint('students_assignments', __name__)


@students_assignments.route('')
def list_students_assignments():
    session = get_session()
    students_assignment = session.query(Student_Assignment).all()
    res = [s.asdict() for s in students_assignment]
    return jsonify(res)


@students_assignments.route(
    '/<int:student_id>/<int:assignment_id>')
def get_student_assignment(student_id, assignment_id):
    session = get_session()
    student_assignment = session.query(Student_Assignment).filter(
        Student_Assignment.student_id == student_id).filter(
        Student_Assignment.assignment_id == assignment_id).first()
    if student_assignment is None:
        abort(404, "There's no such student_id or assignment_id")
    return jsonify(student_assignment.asdict())


@students_assignments.route('', methods=['POST'])
def create_student_assignment():
    student_ass_j = request.get_json()
    if "id" in student_ass_j:
        abort(422)
    session = get_session()
    try:
        student_ass = Student_Assignment.from_dict(student_ass_j)
        session.add(student_ass)
        session.commit()
    except () as error:
        abort(422, error)
    return jsonify(student_ass.asdict()), 201


@students_assignments.route('', methods=['PUT'])
def update_student_assignment():
    student_ass_j = request.get_json()
    if "student_id" not in student_ass_j or "assignment_id" not in student_ass_j:
        abort(422, "student_id or assignment_id hasn't been found")
    session = get_session()
    student_ass = session.query(Student_Assignment).get(
        {"student_id": student_ass_j["student_id"],
         "assignment_id": student_ass_j["assignment_id"]})
    if student_ass is None:
        abort(404, "There's no such student_id or assignment_id")
    try:
        student_ass.update(student_ass_j)
        session.commit()
    except () as error:
        abort(422, error)

    return jsonify(student_ass.asdict()), 200


@students_assignments.route(
    '/<int:student_id>/<int:assignment_id>',
    methods=['DELETE'])
def delete_student_assignment(student_id, assignment_id):
    session = get_session()
    student_ass = session.query(Student_Assignment).get({
        "student_id": student_id,
        "assignment_id": assignment_id
    })
    if student_ass is None:
        abort(404, "There's no such student_id or assignment_id")
    session.delete(student_ass)
    session.commit()
    return Response('', status=200, mimetype='application/json')
