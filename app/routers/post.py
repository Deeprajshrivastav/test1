from .. import schemas, models,utils, oath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
import json
router = APIRouter(
    prefix='/post',
    tags=['Post']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_post(response: Response, db:Session = Depends(get_db), limit:int = 10, skip:int = 0, search:Optional[str] = "", current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts""")
    # data = cursor.fetchone()
    
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, 
            isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        
    return posts

@router.get('/mypost', response_model=List[schemas.PostOut])
def my_post(db:Session=Depends(get_db), current_user: str=Depends(oath2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, 
            isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).all()
        
    return posts

@router.get('/{id}', response_model=schemas.PostOut)
def get_post_by_id(id: int, db:Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute('SELECT * FROM posts WHERE id = {}'.format(id))
    # post = cursor.fetchall()
    # if not post:
    #     raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    post = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(
            models.Votes, models.Votes.post_id == models.Post.id, 
            isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    
    return post

# @app.post('/createposts')
# def create_posts(payload: Post=Body(...)):
#     return payload

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(payload: schemas.CreatePost, db:Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute("""  INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payload.title, payload.content, payload.published))
    # data = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(user_id=current_user.id, **payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db:Session = Depends(get_db), current_user: str = Depends(oath2.get_current_user)):
    # cursor.execute('delete from posts where id = {} RETURNING *'.format(id))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    #print(post.id)
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    post.delete(synchronize_session=False)
    db.commit()
    #conn.commit()
    
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db:Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # if updated_post == None:
    #     raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    # conn.commit()
    print(post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    if update_post == None:
        raise HTTPException(detail='No post found with id {} '.format(id), status_code=status.HTTP_404_NOT_FOUND)
    
    if post.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    post_query.update(post.dict(), synchronize_session=False)
    #print(update_post.first())
    db.commit()
    return post_query.first()


