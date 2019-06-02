from flask import Flask

from students_controller import students
from cohorts_controller import cohorts
from assignments_controller import assignments
from student_assgnments_controller import students_assignments
from student_summary_controller import student_summary
from pets_controller import pets
from transport_types_controller import transport_types
# from rest_application.students.controller import students
# from rest_application.students.controller import students
# from rest_application.students.controller import students
# from rest_application.students.controller import students


# import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from rest_applications.students import students

from data import Assignment, Base, connection, Pet, Cohort, Transport_Type, Student, Student_Assignment

app = Flask(__name__)



app.register_blueprint(students, url_prefix='/students')
app.register_blueprint(cohorts, url_prefix='/cohorts')
app.register_blueprint(assignments, url_prefix='/assignments')
app.register_blueprint(pets, url_prefix='/pets')
app.register_blueprint(students_assignments,
                       url_prefix='/students_assignments')
app.register_blueprint(student_summary, url_prefix='/student_summary')
app.register_blueprint(transport_types, url_prefix='/transport_types')


app.config["JSON_SORT_KEYS"] = False






if __name__ == '__main__':
    app.run(debug=True)
