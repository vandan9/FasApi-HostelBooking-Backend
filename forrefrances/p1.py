from fastapi import FastAPI, HTTPException, Depends, Path, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import date, datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Hostel, Booking, Review, Payment, Fee

app = FastAPI()

# Define the database models (assuming SQLAlchemy is used)
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class RoleEnum(str, Enum):
    admin = "admin"
    hostel_owner = "hostel_owner"
    customer = "customer"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

class HostelBase(BaseModel):
    name: str
    address: str
    description: Optional[str] = None

class HostelCreate(HostelBase):
    owner_id: int

class HostelUpdate(HostelBase):
    pass

class HostelResponse(HostelBase):
    hostel_id: int
    owner_id: int
    created_at: datetime

class BookingBase(BaseModel):
    hostel_id: int
    customer_id: int
    check_in_date: date
    check_out_date: date
    status: Optional[str] = "pending"

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None

class BookingResponse(BookingBase):
    booking_id: int
    created_at: datetime

class ReviewBase(BaseModel):
    hostel_id: int
    customer_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    review_id: int
    created_at: datetime

class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    status: Optional[str] = "pending"
    modified_by: Optional[int] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = None

class PaymentResponse(PaymentBase):
    payment_id: int
    modified_at: datetime

class FeeBase(BaseModel):
    hostel_id: int
    amount: float
    description: Optional[str] = None

class FeeCreate(FeeBase):
    pass

class FeeResponse(FeeBase):
    fee_id: int
    created_at: datetime

# Admin functionalities

# User Management
@app.post("/admin/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/admin/users", response_model=List[UserResponse])
def view_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.put("/admin/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/admin/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# Hostel Management
@app.put("/admin/hostels/{hostel_id}/approve", response_model=HostelResponse)
def approve_hostel(hostel_id: int, db: Session = Depends(get_db)):
    db_hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if db_hostel is None:
        raise HTTPException(status_code=404, detail="Hostel not found")
    db_hostel.approved = True
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

@app.put("/admin/hostels/{hostel_id}/reject", response_model=HostelResponse)
def reject_hostel(hostel_id: int, db: Session = Depends(get_db)):
    db_hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if db_hostel is None:
        raise HTTPException(status_code=404, detail="Hostel not found")
    db_hostel.approved = False
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

@app.get("/admin/hostels", response_model=List[HostelResponse])
def view_hostels(db: Session = Depends(get_db)):
    return db.query(Hostel).all()

# Booking Management
@app.get("/admin/bookings", response_model=List[BookingResponse])
def view_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@app.put("/admin/bookings/{booking_id}", response_model=BookingResponse)
def update_booking_status(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking.dict(exclude_unset=True).items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Review Management
@app.get("/admin/reviews", response_model=List[ReviewResponse])
def view_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@app.delete("/admin/reviews/{review_id}", response_model=ReviewResponse)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return db_review

# Fee Management
@app.post("/admin/fees", response_model=FeeResponse)
def set_fees(fee: FeeCreate, db: Session = Depends(get_db)):
    db_fee = Fee(**fee.dict())
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee

@app.get("/admin/fees", response_model=List[FeeResponse])
def view_fees(db: Session = Depends(get_db)):
    return db.query(Fee).all()

# Hostel Owner Functionalities

# Hostel Management
@app.post("/owner/hostels", response_model=HostelResponse)
def create_hostel(hostel: HostelCreate, db: Session = Depends(get_db)):
    db_hostel = Hostel(**hostel.dict())
    db.add(db_hostel)
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

@app.get("/owner/hostels", response_model=List[HostelResponse])
def view_hostels_owner(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Hostel).filter(Hostel.owner_id == owner_id).all()

@app.put("/owner/hostels/{hostel_id}", response_model=HostelResponse)
def update_hostel(hostel_id: int, hostel: HostelUpdate, db: Session = Depends(get_db)):
    db_hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if db_hostel is None:
        raise HTTPException(status_code=404, detail="Hostel not found")
    for key, value in hostel.dict(exclude_unset=True).items():
        setattr(db_hostel, key, value)
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

@app.delete("/owner/hostels/{hostel_id}", response_model=HostelResponse)
def delete_hostel(hostel_id: int, db: Session = Depends(get_db)):
    db_hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if db_hostel is None:
        raise HTTPException(status_code=404, detail="Hostel not found")
    db.delete(db_hostel)
    db.commit()
    return db_hostel

# Booking Management
@app.get("/owner/bookings", response_model=List[BookingResponse])
def view_bookings_owner(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).join(Hostel).filter(Hostel.owner_id == owner_id).all()

@app.put("/owner/bookings/{booking_id}/confirm", response_model=BookingResponse)
def confirm_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.status = "confirmed"
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.put("/owner/bookings/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.status = "cancelled"
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Payment Management
@app.put("/owner/payments/{payment_id}", response_model=PaymentResponse)
def update_payment_status(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/owner/payments", response_model=List[PaymentResponse])
def view_payments_owner(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Payment).join(Booking).join(Hostel).filter(Hostel.owner_id == owner_id).all()

# Fee Management
@app.get("/owner/fees", response_model=List[FeeResponse])
def view_fees_owner(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Fee).join(Hostel).filter(Hostel.owner_id == owner_id).all()

# Customer Functionalities

# User Profile Management
@app.put("/customer/profile", response_model=UserResponse)
def update_profile(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/customer/profile", response_model=UserResponse)
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# Hostel Search and Booking
@app.get("/hostels", response_model=List[HostelResponse])
def search_hostels(filters: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Hostel)
    # Apply filters logic here
    return query.all()

@app.post("/customer/bookings", response_model=BookingResponse)
def book_hostel(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/customer/bookings", response_model=List[BookingResponse])
def view_bookings_customer(customer_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.customer_id == customer_id).all()

@app.put("/customer/bookings/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking_customer(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.status = "cancelled"
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Review Management
@app.post("/customer/reviews", response_model=ReviewResponse)
def leave_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/customer/reviews", response_model=List[ReviewResponse])
def view_reviews_customer(customer_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.customer_id == customer_id).all()

@app.put("/customer/reviews/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review: ReviewBase, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review.dict(exclude_unset=True).items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

# Payment Management
@app.post("/customer/payments", response_model=PaymentResponse)
def make_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/customer/payments", response_model=List[PaymentResponse])
def view_payments_customer(customer_id: int, db: Session = Depends(get_db)):
    return db.query(Payment).join(Booking).filter(Booking.customer_id == customer_id).all()
