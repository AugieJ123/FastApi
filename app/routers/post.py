from sqlalchemy import func
# import models, schemas, oauth2  # For development
from typing import List
from fastapi import  Response, status, HTTPException, Depends, APIRouter
# from database import get_db
from sqlalchemy.orm import Session

# For production...
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['Post'])

@router.get("/", response_model=List[schemas.PostLikeOut])
def get_posts(db: Session = Depends(get_db), limit: int = 100, skip: int = 0, search:str = ""):

    result  = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
                        isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)
                        ).limit(limit).offset(skip).all()
 
    return result

# Get all post by a particular user
@router.get("/user/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
 
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostLikeOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
                        isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_post_query.first()

    if not delete_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_ = post_query.first()

    if not post_:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
