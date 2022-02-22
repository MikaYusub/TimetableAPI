from sqlalchemy import CheckConstraint, Column, Time, UniqueConstraint
from sqlalchemy import Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Timetable(Base):

    __tablename__ = "timetable3"
    id = Column(Integer, primary_key=True)
    classtime_id = Column(Integer, ForeignKey(
        "classtime.id"), nullable=False)
    dayofweek = Column(Integer, ForeignKey(
        "dayofweek.dayofweek"), nullable=False)
    ctime = relationship("Classtime")

    event_id = Column(Integer, ForeignKey(
        "teacher_subject_grade.id"))

    event = relationship('Teacher_Subject_Grade')


class Teacher_Subject_Grade(Base):
    __tablename__ = "teacher_subject_grade"
    __table_args__ = (
        UniqueConstraint('subject_id', 'teacher_id', 'grade_id'),
    )
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grade.id"), nullable=False)
    grade = relationship('Grade')
    teacher = relationship('Teacher')
    subject = relationship('Subject')


class DayOfWeek(Base):
    # dayofweek
    # 1
    # 2
    # 3
    # .
    __tablename__ = "dayofweek"
    __table_args__ = (
        CheckConstraint('0 < dayOfWeek'),
        CheckConstraint('dayOfWeek <= 5')
    )
    dayofweek = Column(Integer, primary_key=True)


class Classtime(Base):
    # id | startTime | endTime
    # 1     08:00       08:45
    # 2     08:50       09:35
    # 3     09:40       10:25
    # .      ....       .....
    __tablename__ = "classtime"

    id = Column(Integer, primary_key=True)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)


class Grade(Base):

    # id | year | ext
    # 1     7      A
    # 2     7      B
    # 3     8      C

    __tablename__ = "grade"
    __table_args__ = (
        CheckConstraint('0 < year'),
        CheckConstraint('year <= 11'),
        UniqueConstraint('year', 'ext')
    )

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    ext = Column(String(1), nullable=False)


class Subject(Base):
    # id | name
    # 1    Literature
    # 2    Physics
    # .     .....
    __tablename__ = "subject"
    __table_args__ = (
        UniqueConstraint('name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Teacher(Base):
    # id | name | surname
    # 1    Marie    Curie
    # 2    Mammad   Mammadov
    # .     .....   ......
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
