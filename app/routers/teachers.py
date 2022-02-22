from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app import models
from app import schemas

from app.schemas import TeacherBase
from ..database import get_db

router = APIRouter(
    prefix="/teacher",
    tags=['Teacher']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherBase, db: Session = Depends(get_db)):
    try:
        new_teacher = models.Teacher(**teacher.dict())
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return new_teacher
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.get("/{teacher_id}")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(models.Teacher).filter(
            models.Teacher.id == teacher_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):

    teacher_query = db.query(models.Teacher).filter(
        models.Teacher.id == teacher_id)

    teacher = teacher_query.first()

    if teacher == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"teacher with id: {teacher_id} does not exist")

    if db.query(models.Teacher_Subject_Grade).filter(
            models.Teacher_Subject_Grade.teacher_id == teacher_id).all() == None:
        teacher_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="Can't delete this teacher because this teacher still has references in joint events table")


@router.put("/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, updated_teacher: schemas.TeacherBase,
                   db: Session = Depends(get_db)):

    teacher_query = db.query(models.Teacher).filter(
        models.Teacher.id == teacher_id)
    teacher = teacher_query.first()

    if teacher == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"teacher with id: {teacher_id} does not exist")

    teacher_query.update(updated_teacher.dict(), synchronize_session=False)

    db.commit()

    return teacher_query.first()
