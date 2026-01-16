from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from .. import oauth2
from ..database import get_db

router = APIRouter(prefix="/post", tags=["Post"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    Limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    results = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(Limit)
        .offset(skip)
        .all()
    )
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if post:
        post_dict = post.dict()
        new_post = models.Post(owner_id=current_user.id, **post_dict)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/{id}", response_model=schemas.Post)
def get_one(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # one_post=cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()  # type:ignore
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )

    return post


@router.delete("/{id}", response_model=schemas.Post)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s """,(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post_query = (
        db.query(models.Post).filter(models.Post.id == id).first()
    )  # type:ignore
    post = post_query.first()
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with Id: {id}"
        )
    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Please Log In"
        )

    db.delete(post_query)
    db.commit()

    return post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostUpdate)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    updated_post = db.query(models.Post).filter(models.Post.id == id)  # type:ignore
    updated = updated_post.first()
    if updated == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with Id:{id}"
        )
    if updated.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Log in")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated)
    return updated
