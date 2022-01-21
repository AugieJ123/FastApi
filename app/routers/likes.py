from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# For development...
# import schemas, database, models, oauth2

# For production...
from .. import database, schemas, models, oauth2

router = APIRouter(prefix="/like", tags=['Like'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    like_query = db.query(models.Vote).filter(models.Vote.post_id == like.post_id, models.Vote.user_id == current_user.id)
    found_like = like_query.first()

    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has alreadylike a post {like.post_id}")
        new_like = models.Vote(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()

        return {"message": "successfully added a like"}

    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"User {current_user.id} has not liked a post {like.post_id}")
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully delete a like"}
