from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data import Assignment, Base, connection, Pet, Cohort, Transport_Type, Student, Student_Assignment
def get_session():
    engine = create_engine(
        'mysql://{username}:{password}@{host}/{db_name}?charset=utf8mb4'.format(
            username=connection["USERNAME"],
            password=connection["PASSWORD"],
            host=connection["HOST"],
            db_name=connection["DB_NAME"]
        )
    )
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
