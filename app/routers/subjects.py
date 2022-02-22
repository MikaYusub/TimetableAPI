
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models

from app.schemas import SubjectBase
from ..database import get_db

router = APIRouter(
    prefix="/timetable",
    tags=['Subject']
)


@router.post("/subject", status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectBase, db: Session = Depends(get_db)):
    try:
        new_subject = models.Subject(**subject.dict())
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        return new_subject
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")
