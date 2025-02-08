from unittest import result
from .load import *
from ..oath2 import get_current_user
from typing import List
router=APIRouter(
    prefix="/booking",
    tags=["booking"]
)


@router.post("/add_booking",status_code=status.HTTP_201_CREATED)
def add_router(booking:schemas.Booking,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    new_booking=models.bookings(**booking.dict(),customer_id=current_user.user_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.delete("/delete_booking/{booking_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    booking=db.query(models.bookings).filter(models.bookings.booking_id==booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="booking not found")
    db.delete(booking)
    db.commit()

    return {"message":"booking deleted"}

@router.get("/view_bookings")
def view_bookings(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
     bookings=db.query(models.bookings).filter(models.bookings.customer_id==current_user.user_id).all()
     return bookings
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="servererror")


@router.get("/view_all_bookings/{hostel_id}", response_model=List[schemas.UserWithBookings])
def view_all_bookings(hostel_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    role = str(current_user.role).split(".")[1]
    if role == "hostel_owner":
        results = db.query(
            models.Users.user_id,
            models.Users.username,
            models.bookings.booking_id,
            models.bookings.hostel_id,
            models.bookings.check_in,
            models.bookings.check_out
        ).join(
            models.bookings, models.bookings.customer_id == models.Users.user_id
        ).filter(
            models.bookings.hostel_id == hostel_id
        ).all()
        users = {}
        for result in results:
            user_id, username, booking_id, hostel_id, check_in, check_out = result
            if user_id not in users:
                users[user_id] = {
                    "user_id": user_id,
                    "username": username,
                    "bookings": []
                }
            users[user_id]["bookings"].append({
                "booking_id": booking_id,
                "hostel_id": hostel_id,
                "check_in": check_in,
                "check_out": check_out
            })
        
        return [schemas.UserWithBookings(**user) for user in users.values()]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

   