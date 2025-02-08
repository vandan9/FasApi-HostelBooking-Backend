from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status,Depends
from . import models  # Import your SQLAlchemy models
from .database import get_db  # Adjust import path as per your project
from .oath2 import get_current_user  # Adjust import path as per your project

class Review:
    def __init__(self, review_id: int):
        self.review_id = review_id
    
    def update_review(self, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
        rating = db.query(func.avg(models.Vote.ratting)).filter(models.Vote.reviwe_id == self.review_id).scalar()
        
        db_review = db.query(models.Review).filter(models.Review.review_id == self.review_id).first()
        if not db_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        
        db_review.rating = rating
        db.commit()
        db.refresh(db_review)
        
        # Optionally, return the updated review object
