from datetime import time
from pydantic import BaseModel


class ClasstimeBase(BaseModel):
    startTime: time
    endTime: time

    class Config:
        orm_mode = True


class Classtime(ClasstimeBase):
    id: int

    class Config:
        orm_mode = True


class GradeBase(BaseModel):
    year: int
    ext: str

    class Config:
        orm_mode = True


class Grade(GradeBase):
    id: int

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Subject(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class Event(BaseModel):
    id: int
    subject_id: int
    teacher_id: int
    grade_id: int
    grade: Grade
    teacher: Teacher
    subject: Subject

    class Config:

        orm_mode = True


class EventCreate(BaseModel):
    subject_id: int
    teacher_id: int
    grade_id: int

    class Config:

        orm_mode = True


class EventOut(BaseModel):
    grade: Grade
    teacher: Teacher
    subject: Subject

    class Config:

        orm_mode = True


class DayOfWeek(BaseModel):
    dayofweek: int

    class Config:

        orm_mode = True


class Timetable(BaseModel):
    id: int
    classtime_id: int
    ctime: ClasstimeBase
    event_id: int
    event: EventOut
    dayofweek: int

    class Config:

        orm_mode = True


class TimetableCreate(BaseModel):
    classtime_id: int
    event_id: int
    dayofweek: int

    class Config:

        orm_mode = True
