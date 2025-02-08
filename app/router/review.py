
from typing import List

from sqlalchemy import func

from app.schemas import review
from .load import *

router=APIRouter(
   prefix="/review",
   tags=["review"]  
)

@router.post("/add_review",status_code=status.HTTP_201_CREATED)
def add_review(review:schemas.review,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    role=str(current_user.role).split(".")[1]
    if(role=="hostel_owner"):
        new_review=models.Review(**review.dict(),rating=0)
        db.add(new_review)
        db.commit()
        db.refresh
        return new_review 
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    
@router.delete("/delete_review/{review_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    role=str(current_user.role).split(".")[1]
    if(role=="hostel_owner"):
        db_review=db.query(models.Review).filter(models.Review.revieew_id==review_id).first()
        if not db_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="review not found")
        db.delete(db_review)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
  
@router.get("/bookinghostel",response_model=List[schemas.review])
def bookinghostel(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    bookingshostel=db.query(models.bookings.hostel_id).filter(models.Booking.customer_id==current_user.user_id).all()
    review=db.query(models.Review).filter(models.Review.hostel_id.in_(bookingshostel)).all()
    return review

@router.get("/details/{hostel_id}",response_model=List[schemas.reviewdetails])
def details(hostel_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    review=db.query(models.Review).filter(models.Review.hostel_id==hostel_id).all()
    print(type(review))
    for r1 in review:
     rate=db.query(func.avg(models.Vote.ratting)).group_by(models.Vote.reviwe_id).filter(models.Vote.reviwe_id==r1.review_id).scalar()
     if rate is not None:
        r1.rating=rate
     else:
        r1.rating=0
    return review

