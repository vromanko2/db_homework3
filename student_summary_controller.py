from flask import Blueprint, abort, jsonify,request,Response

from data import Student
from get_session import get_session
student_summary = Blueprint('student_summary', __name__)
@student_summary.route('')
def list_student_summaries():
    session = get_session()
    res = session.execute("SELECT * from student_summary").fetchall()
    res = [dict(zip(("id", "first_name", "last_name", "dormitory", "cohort", "pet", "transport", "mean_assignment_value"), row)) for row in res]
    return jsonify(res)


@student_summary.route('/<int:id>')
def get_student_summary(id):
    session = get_session()
    res = session.execute("SELECT * from student_summary WHERE id=:id", {"id" : id}).fetchone()
    if res is None:
        abort(404, "There's no such student id")
    res = dict(zip(("id", "first_name", "last_name", "dormitory", "cohort", "pet", "transport", "mean_assignment_value"), res))
    return jsonify(res)

