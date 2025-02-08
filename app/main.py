from fastapi import FastAPI

from app.router import vote
from . import models
from .database import engine
from .router import user,auth,hostel,review,payment,booking

# models.Base.metadata.create_all(bind=engine) this is useful for only sqlalchemy models and not alembic

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(hostel.router)
app.include_router(review.router)
app.include_router(payment.router)
app.include_router(vote.router)
app.include_router(booking.router)