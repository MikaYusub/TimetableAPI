
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.schemas import GradeBase
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/grades",
    tags=['Grades']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_grade(grade: GradeBase, db: Session = Depends(get_db)):
    try:
        new_grade = models.Grade(**grade.dict())
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        return new_grade
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")


@router.get("/{grade_id}")
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(models.Grade).filter(
            models.Grade.id == grade_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):

    grade_query = db.query(models.Grade).filter(
        models.Grade.id == grade_id)

    grade = grade_query.first()

    if grade == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"grade with id: {grade_id} does not exist")

    if db.query(models.Teacher_Subject_Grade).filter(
            models.Teacher_Subject_Grade.grade_id == grade_id).all() == None:
        grade_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Can't delete this grade because this grade still has references in joint events table")


@router.put("/{grade_id}", response_model=schemas.Grade)
def update_grade(grade_id: int, updated_grade: schemas.GradeBase,
                 db: Session = Depends(get_db)):

    grade_query = db.query(models.Grade).filter(
        models.Grade.id == grade_id)
    grade = grade_query.first()

    if grade == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"grade with id: {grade_id} does not exist")

    grade_query.update(updated_grade.dict(), synchronize_session=False)

    db.commit()

    return grade_query.first()
