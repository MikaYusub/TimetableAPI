from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app import models
from app import schemas
from ..database import get_db

router = APIRouter(
    prefix="/timetable",
    tags=['Timetable']
)


@router.post("/event", status_code=status.HTTP_201_CREATED)
def create_event_item(tt: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        new_event_obj = models.Teacher_Subject_Grade(**tt.dict())
        db.add(new_event_obj)
        db.commit()
        db.refresh(new_event_obj)
        return new_event_obj
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.put("/event/{event_id}", status_code=status.HTTP_201_CREATED)
def update_event(event_id: int, updated_event: schemas.EventCreate,
                 db: Session = Depends(get_db)):
    event_query = db.query(models.Teacher_Subject_Grade).filter(
        models.Teacher_Subject_Grade.id == event_id)
    event = event_query.first()
    if event == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"event with id: {event_id} does not exist")

    event_query.update(updated_event.dict(), synchronize_session=False)

    db.commit()

    return event_query.first()


@router.delete("/event/{event_id}", status_code=status.HTTP_201_CREATED)
def delete_event(event_id: int, db: Session = Depends(get_db)):

    event_query = db.query(models.Teacher_Subject_Grade).filter(
        models.Teacher_Subject_Grade.id == event_id)

    event = event_query.first()

    if event == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"event with id: {event_id} does not exist")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_timetable_item(tt: schemas.TimetableCreate, db: Session = Depends(get_db)):
    new_timetable_obj = models.Timetable(**tt.dict())
    db.add(new_timetable_obj)
    db.commit()
    db.refresh(new_timetable_obj)
    return new_timetable_obj


@router.get("/", response_model=List[schemas.Timetable])
def get_timetable(db: Session = Depends(get_db)):
    all_timetable = db.query(models.Timetable).all()
    return all_timetable


@router.get("/teacher/{teacher_id}", response_model=List[schemas.Timetable])
def get_timetable_for_teacher(teacher_id: int, db: Session = Depends(get_db)):
    tt_query = db.query(
        models.Teacher_Subject_Grade).filter(
        models.Teacher_Subject_Grade.teacher_id == teacher_id).with_entities(
            models.Teacher_Subject_Grade.id)

    try:
        return db.query(models.Timetable).filter(
            models.Timetable.event_id.in_([value[0] for value in tt_query])).all()

    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.get("/grade/{grade_id}", response_model=List[schemas.Timetable])
def get_timetable_for_grade(grade_id: int, db: Session = Depends(get_db)):
    tt_query = db.query(
        models.Teacher_Subject_Grade).filter(
        models.Teacher_Subject_Grade.grade_id == grade_id).with_entities(
            models.Teacher_Subject_Grade.id)

    try:
        return db.query(models.Timetable).filter(
            models.Timetable.event_id.in_([value[0] for value in tt_query])).all()

    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.get("/subject/{subject_id}", response_model=List[schemas.Timetable])
def get_timetable_for_subject(subject_id: int, db: Session = Depends(get_db)):
    tt_query = db.query(
        models.Teacher_Subject_Grade).filter(
        models.Teacher_Subject_Grade.subject_id == subject_id).with_entities(
            models.Teacher_Subject_Grade.id)

    try:
        return db.query(models.Timetable).filter(
            models.Timetable.event_id.in_([value[0] for value in tt_query])).all()

    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")
