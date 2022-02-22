
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
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
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")
