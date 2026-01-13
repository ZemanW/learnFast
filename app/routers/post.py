from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from .. import oauth2
from ..database import get_db

router = APIRouter(prefix="/post", tags=["Post"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if post:
        post_dict = post.dict()
        new_post = models.Post(**post_dict)
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
    post = db.query(models.Post).filter(models.Post.id == id).first()  # type:ignore

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with Id: {id}"
        )

    db.delete(post)
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
    print(updated_post)
    if updated == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with Id:{id}"
        )

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated)
    return updated
