from .load import *
from ..updatereview import Review
router=APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/add_vote/{review_id}/{ratting}",status_code=status.HTTP_201_CREATED)
def add_vote(review_id:int,ratting:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    new_vote=models.Vote(customer_id=current_user.user_id,reviwe_id=review_id,ratting=ratting)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    updatevote=Review(review_id)
    updatevote.update_review(db)
    return new_vote
