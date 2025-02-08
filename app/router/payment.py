from sqlalchemy import true
from .load import *
from ..oath2 import get_current_user
from typing import List
from .. import schemas,models
router = APIRouter(
    prefix="/payment",
    tags=['payment']
)

@router.put("/add/{id}",status_code=status.HTTP_201_CREATED)
def paymentDone(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    new_payment=db.query(models.bookings).filter(models.bookings.booking_id==id).first()
    if not new_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")
    new_payment.payment=True
    db.commit()

    return {"massage : payment add successfully"}

@router.put("/clear/{id}",status_code=status.HTTP_201_CREATED)
def paymentDone(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    new_payment=db.query(models.bookings).filter(models.bookings.booking_id==id).first()
    if not new_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")
    new_payment.payment=False
    db.commit()

    return {"massage : payment deleted successfully"}


@router.put("/delete/{hostelid}",status_code=status.HTTP_201_CREATED)
def paymentDone(hostelid:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    new_payment=db.query(models.bookings).filter(models.bookings.hostel_id==hostelid).all()
    if not new_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")
    for i in new_payment:
        i.payment=False 
    db.commit()

    return {"massage : payment all payment clear"}
  
@router.get("/panding/{hostel_id}", response_model=List[schemas.UserWithBookings])
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
            models.bookings.hostel_id == hostel_id,
            models.bookings.payment == False
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
    
@router.get("/done/{hostel_id}", response_model=List[schemas.UserWithBookings])
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
            models.bookings.hostel_id == hostel_id,
            models.bookings.payment == True
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



   

    