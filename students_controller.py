from flask import Blueprint, abort, jsonify,request,Response

from data import Student
from get_session import get_session

students = Blueprint('students', __name__)


@students.route('')
def list_students():
    session = get_session()
    student = session.query(Student).all()
    res = [c.asdict() for c in student]
    return jsonify(res)


@students.route('/<int:id>')
def get_student(id):
    session = get_session()
    student = session.query(Student).filter(Student.id == id).first()
    if student is None:
        abort(404, "There's no such student id")
    return jsonify(student.asdict())


@students.route('', methods=['POST'])
def create_student():
    student_j = request.get_json()
    if "id" in student_j:
        abort(422)
    session = get_session()
    try:
        print("HERE")
        student = Student.from_dict(student_j)
        session.add(student)
        session.commit()
    except () as error:
        abort(422, error)
    return jsonify(student.asdict()), 201



@students.route('', methods=['PUT'])
def update_student():
    student_j = request.get_json()
    if "id" not in student_j:
        abort(422, "There's no such id")
    session = get_session()
    student = session.query(Student).get(student_j["id"])
    if student is None:
        abort(404, "There's no student with such id")
    try:
        student.update(student_j)
    except () as error:
        abort(422, error)
    session.commit()
    return jsonify(student.asdict()), 200


@students.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    session = get_session()
    student = session.query(Student).get(id)
    if student is None:
        abort(404, "There's no such student id")
    session.delete(student)
    session.commit()
    return Response('', status=200, mimetype='application/json')
