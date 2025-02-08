from .load import *
from ..schemas import Ragisterin,EmailSchema
from ..utils import hash
from ..email import send_otp, verify_otp



router =APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register")
async def register(user:Ragisterin,status_code=status.HTTP_201_CREATED,db:Session=Depends(get_db)):
  
    # Check if username already exists
    existing_user_username = db.query(models.Users).filter(models.Users.username == user.username).first()
    if existing_user_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_user_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user_email:
        raise HTTPException(status_code=400, detail="Email already exists")
  
    try:
        user.password = hash(user.password)
        new_user = models.Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # await send_otp(user.email)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
    return {"message": "account created successfully"}
   
    

@router.post("/verify")
async def verify(otp:EmailSchema,db:Session=Depends(get_db)):
     if verify_otp(otp.email,otp.otp):
        db.query(models.Users).filter(models.Users.email==otp.email).update({"is_active":True})
        db.commit()
        return {"massage":"user is active"}
     return {"massage":"invalid otp"}