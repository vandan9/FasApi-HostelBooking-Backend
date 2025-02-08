from typing import List
from .load import *
from ..oath2 import get_current_user

router=APIRouter(
    prefix="/hostel",
    tags=["hostel"]
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(hostel:schemas.hostel,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    role=str(current_user.role).split(".")[1]
    print(role)
    if(role=="admin" or role=="hostel_owner"):
        new_hostel=models.Hostels(owner_id=current_user.user_id,**hostel.dict())
        db.add(new_hostel)
        db.commit()
        db.refresh(new_hostel)
        return new_hostel
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    
@router.get("/owend_hostel")
def get_hostel(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    role=str(current_user.role).split(".")[1]
    if(role=="admin" or role=="hostel_owner"):
        hosteldata= db.query(models.Hostels).filter(models.Hostels.owner_id==current_user.user_id).all()
        return hosteldata
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    
@router.delete("/delete_hostel/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hostel(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    hostel_delete = db.query(models.Hostels).filter(models.Hostels.hostel_id == id).first()
    if not hostel_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hostel not found")
    elif not hostel_delete.owner_id == current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    else:
     db.delete(hostel_delete)
     db.commit()
     return {"message": "Hostel deleted"}
    
@router.put("/update_hostel/{id}",status_code=status.HTTP_200_OK)
def update_hostel(id:int,updata:schemas.updata,db:Session = Depends(get_db),current_user=Depends(get_current_user)):
     update_hostel=db.query(models.Hostels).filter(models.Hostels.hostel_id==id)
     data=update_hostel.first()
     if update_hostel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="hostel not found")
     if data.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not aurhorized perform this action") 
     update_hostel.update(updata.dict(),synchronize_session=False)
     db.commit()
     return {"update sucessfully"}
    
@router.get("/search",status_code=status.HTTP_200_OK,response_model=List[schemas.hostel])
def search_hostel(db:Session=Depends(get_db)):
      hostel=db.query(models.Hostels).all()
      return hostel
