from subprocess import check_output
from pydantic import Field
from pydantic import BaseModel, EmailStr
from datetime import datetime



class Ragisterin(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str

class EmailSchema(BaseModel):
    email:EmailStr
    otp:str
class login(BaseModel):
    username:str
    password:str

class hostel(BaseModel):
    name:str
    address:str
    description: str = Field(..., description="Description of the hostel", max_length=1000)
    fees:int

    # class Config:
    #     from_attributes = True
class updata(BaseModel):
    name:str
    address:str
    description:str
    fees:int

class review(BaseModel):
    hostel_id:int
    comment:str

class Booking(BaseModel):
    hostel_id:int
    check_in:datetime
    check_out:datetime

class Payment(BaseModel):
    booking_id:int

class bookinghostelreview(BaseModel):
    hostelname:str

class reviewdetails(review):
    review_id:int
    rating:int
    create_at:datetime
    hostel_id:int
 
# class review_details(reviewdetails):
#     review: List[reviewdetails] 

#     class Config:
#         orm_mode = True
class BookingBase(BaseModel):
    booking_id: int
    hostel_id: int
    check_in: datetime
    check_out: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    user_id: int
    username: str

    class Config:
        orm_mode = True
from typing import List
class UserWithBookings(UserBase):
    bookings: List[BookingBase] 

    class Config:
        orm_mode = True