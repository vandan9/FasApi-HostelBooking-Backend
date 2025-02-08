from app.router import payment
from .database import Base
from sqlalchemy import Boolean, Column,Integer,String, column, false,ForeignKey,Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Enum as EnumType
from enum import Enum

class RoleEnum(Enum):
    admin = 'admin'
    hostel_owner = 'hostel_owner'
    customer = 'customer'

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    is_active=Column(Boolean,server_default=false(),nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(EnumType(RoleEnum), nullable=False)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))


class Hostels(Base):
    __tablename__ = 'hostels'

    hostel_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    fees = Column(Integer, nullable=True, server_default=text('0'))
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    hostel_id = Column(Integer, ForeignKey('hostels.hostel_id'))
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=False)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

class Vote(Base):
    __tablename__="votes"

    vote_id= Column(Integer, primary_key=True, autoincrement=True)
    customer_id=Column(Integer, ForeignKey('users.user_id'))
    reviwe_id=Column(Integer, ForeignKey('reviews.review_id'))
    ratting=Column(Integer, nullable=True)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

class bookings(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('users.user_id'))
    hostel_id = Column(Integer, ForeignKey('hostels.hostel_id'))
    check_in = Column(TIMESTAMP(timezone=True), nullable=False)
    check_out = Column(TIMESTAMP(timezone=True), nullable=False)
    payment=Column(Boolean,server_default=false(),nullable=False)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))





   