from .load import *
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router=APIRouter(
    tags=['Auth']
)

@router.post('/login')
def login(userdetails:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.username==userdetails.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    if not utils.verify(userdetails.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    access_token= oath2.generate_token(data={"user_id":user.user_id})
    return {"access_token":access_token,"token_type":"bearer"}