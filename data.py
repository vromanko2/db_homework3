import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import class_mapper, backref, relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey

Base = declarative_base()


class DictMixin:
    def asdict(self):
        return dict((col.name, getattr(self, col.name))
                    for col in class_mapper(self.__class__).mapped_table.c)

    @classmethod
    def from_dict(cls, value):
        result_ = {}
        for column in class_mapper(cls).mapped_table.c:
            if not column.name == "id":
                if not column.nullable and column.name not in value:
                    raise AttributeError("Missed not null attribute {}".format(column.name))
                elif column.name in value:
                    if not isinstance(value[column.name], column.type.python_type):
                        raise TypeError("Wrong type {} of attribute {}. Type should be {}".format(column.name, type(value[column.name]), column.type.python_type))
                    result_[column.name] = value[column.name]
        return cls(**result_)

    def update(self, value):
        for column in class_mapper(self.__class__).mapped_table.c:
            if not column.name == "id":
                try:
                    if not isinstance(value[column.name], column.type.python_type):
                        raise TypeError ("Wrong type {} of attribute {}. Type should be {}".format(column.name, type(value[column.name]),
                                                column.type.python_type))
                    setattr(self, column.name, value[column.name])
                except KeyError as error:
                    raise AttributeError("Missed {} attribute. Just full update can be done".format(error.args[0]))
                return self


class Pet(Base, DictMixin):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Cohort(Base, DictMixin):
    __tablename__ = "cohorts"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Transport_Type(Base, DictMixin):
    __tablename__ = "transport_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Assignment(Base, DictMixin):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    students = relationship("Student", secondary="students_assignments")


class Student(Base, DictMixin):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    dormitory = Column(Boolean, nullable=False)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    transport_type_id = Column(Integer, ForeignKey("transport_types.id"),nullable=True)
    cohort = relationship(Cohort, backref=backref("students", uselist=True))
    pet = relationship(Pet, backref=backref("students", uselist=True))
    transport_type = relationship(Transport_Type, backref=backref("students", uselist=True))
    assignments = relationship(Assignment, secondary="students_assignments")


class Student_Assignment(Base, DictMixin):
    __tablename__ = "students_assignments"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), primary_key=True)
    value = Column(Float)


# TODO: Set credentials for your user defined in db.sql

connection = {
    "USERNAME": "newuser",
    "PASSWORD": "password",
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "DB_NAME": "university"
}
engine = create_engine(
    'mysql://{username}:{password}@{host}/{db_name}?charset=utf8mb4'.format(
        username=connection["USERNAME"],
        password=connection["PASSWORD"],
        host=connection["HOST"],
        db_name=connection["DB_NAME"]
    )
)


Base.metadata.create_all(engine)