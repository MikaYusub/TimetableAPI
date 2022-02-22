
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app import models
from app import schemas

from app.schemas import SubjectBase
from ..database import get_db

router = APIRouter(
    prefix="/subject",
    tags=['Subject']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.get("/{subject_id}")
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(models.Subject).filter(
            models.Subject.id == subject_id).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid data")


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):

    subject_query = db.query(models.Subject).filter(
        models.Subject.id == subject_id)

    subject = subject_query.first()

    if subject == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"subject with id: {subject_id} does not exist")

    if db.query(models.Teacher_Subject_Grade).filter(
            models.Teacher_Subject_Grade.subject_id == subject_id).all() == None:
        subject_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="Can't delete this subject because this subject still has references in joint events table")


@router.put("/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, updated_subject: schemas.SubjectBase,
                   db: Session = Depends(get_db)):

    subject_query = db.query(models.Subject).filter(
        models.Subject.id == subject_id)
    subject = subject_query.first()

    if subject == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"subject with id: {subject_id} does not exist")

    subject_query.update(updated_subject.dict(), synchronize_session=False)

    db.commit()

    return subject_query.first()
